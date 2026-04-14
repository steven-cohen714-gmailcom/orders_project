# File: backend/endpoints/reports.py
from fastapi import APIRouter, Query, Depends, HTTPException
from typing import Optional, List, Dict, Any
import sqlite3
from datetime import datetime

from backend.database import get_db_connection
from backend.utils.permissions_utils import require_login
from backend.endpoints.order_queries import validate_date

router = APIRouter()

# ---- Status canonicalisation (kept in sync with shared_filters.js) ----
CANONICAL_STATUSES = [
    "Draft", "Pending", "Awaiting Authorisation", "Authorised",
    "Partially Received", "Received", "Partially Paid", "Paid", "Deleted"
]

STATUS_ALIASES = {
    "Review": "Draft",
    "To Review": "Draft",
    "Draft Order": "Draft",
    "Waiting for Approval": "Awaiting Authorisation",
    "Awaiting Authorization": "Awaiting Authorisation",
    "Authorized": "Authorised",
    "Partially Delivered": "Partially Received",
    "Partially Payed": "Partially Paid",
    "Part Paid": "Partially Paid",
    "COD": None,  # not a status
}

def canonicalise(status: Optional[str]) -> Optional[str]:
    if status is None:
        return None
    s = status.strip()
    return STATUS_ALIASES.get(s, s)

def status_synonyms(status: Optional[str]) -> List[str]:
    canon = canonicalise(status)
    if canon is None:
        return []
    syns = {canon}
    for legacy, target in STATUS_ALIASES.items():
        if target == canon:
            syns.add(legacy)
    return sorted(syns)

def _like_or_none(value: Optional[str]) -> Optional[str]:
    if value is None or value.strip().lower() == "all":
        return None
    return f"%{value.strip()}%"

def _append_status_filter(filters: List[str], params: List[Any], status: Optional[str]):
    if status and status.lower() != "all":
        syns = status_synonyms(status)
        if syns:
            placeholders = " OR ".join(["UPPER(o.status) = UPPER(?)"] * len(syns))
            filters.append(f"({placeholders})")
            params.extend(syns)

def _apply_common_filters(filters: List[str], params: List[Any],
                          start_date: Optional[str], end_date: Optional[str],
                          requester: Optional[str], supplier: Optional[str],
                          project: Optional[str], status: Optional[str],
                          only_cod: bool, exclude_deleted: bool):
    # Dates
    if start_date:
        sd = validate_date(start_date)
        if sd:
            filters.append("DATE(o.created_date) >= DATE(?)")
            params.append(sd)
    if end_date:
        ed = validate_date(end_date)
        if ed:
            filters.append("DATE(o.created_date) <= DATE(?)")
            params.append(ed)

    # Requester / Supplier (LIKE)
    req_like = _like_or_none(requester)
    if req_like:
        filters.append("UPPER(r.name) LIKE UPPER(?)")
        params.append(req_like)

    sup_like = _like_or_none(supplier)
    if sup_like:
        filters.append("UPPER(s.name) LIKE UPPER(?)")
        params.append(sup_like)

    # Project (prefer per-line project if present on order_items)
    proj_like = _like_or_none(project)
    if proj_like:
        # both cases covered: if project stored on items or on orders
        filters.append("(UPPER(oi.project) LIKE UPPER(?) OR UPPER(o.project) LIKE UPPER(?))")
        params.extend([proj_like, proj_like])

    # Status (with legacy synonyms)
    _append_status_filter(filters, params, status)

    # Only COD
    if only_cod:
        filters.append("UPPER(o.payment_terms) = 'COD'")

    # Exclude Deleted (default True)
    if exclude_deleted:
        filters.append("UPPER(o.status) <> 'DELETED'")

def _rows_to_dicts(cursor: sqlite3.Cursor) -> List[Dict[str, Any]]:
    cols = [c[0] for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

def _result(columns: List[str], rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Ensure column order
    out_rows = []
    for r in rows:
        out_rows.append({c: r.get(c, "") for c in columns})
    return {"columns": columns, "rows": out_rows}

@router.get("/api/report/line_items")
async def report_line_items(
    group_by: str = Query(..., pattern="^(item|project|supplier|requester|open|partial|cod|variance)$"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requester: Optional[str] = Query(None),
    supplier:  Optional[str] = Query(None),
    project:   Optional[str] = Query(None),
    status:    Optional[str] = Query(None),

    include_details: bool = Query(False),
    group_monthly:   bool = Query(False),
    only_cod:        bool = Query(False),
    show_price_stats:bool = Query(False),
    exclude_deleted: bool = Query(True),

    user: Dict = Depends(require_login),
):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        filters: List[str] = []
        params: List[Any] = []
        _apply_common_filters(filters, params, start_date, end_date, requester, supplier, project, status, only_cod, exclude_deleted)
        where_clause = " AND ".join(filters) if filters else "1=1"

        # --- Routing by group_by ---
        if group_by == "item":
            # Detail rows
            detail_sql = f"""
                SELECT
                    DATE(o.created_date) AS order_date,
                    o.order_number,
                    r.name AS requester,
                    s.name AS supplier,
                    oi.item_code,
                    oi.item_description,
                    COALESCE(oi.project, o.project) AS project,
                    oi.qty_ordered AS quantity,
                    oi.price AS unit_price,
                    oi.total AS line_total
                FROM order_items oi
                JOIN orders o ON o.id = oi.order_id
                LEFT JOIN requesters r ON r.id = o.requester_id
                LEFT JOIN suppliers  s ON s.id = o.supplier_id
                WHERE {where_clause}
                ORDER BY oi.item_code, o.created_date, o.order_number
            """
            detail_cols = ["order_date","order_number","requester","supplier","item_code","item_description","project","quantity","unit_price","line_total"]

            # Summary rows per item
            sum_sql = f"""
                SELECT
                    oi.item_code,
                    oi.item_description,
                    SUM(oi.qty_ordered) AS total_qty,
                    SUM(oi.total) AS total_spend
                    {", AVG(oi.price) AS avg_unit_price, MIN(oi.price) AS min_unit_price, MAX(oi.price) AS max_unit_price" if show_price_stats else ""}
                FROM order_items oi
                JOIN orders o ON o.id = oi.order_id
                WHERE {where_clause}
                GROUP BY oi.item_code, oi.item_description
                ORDER BY total_spend DESC
            """
            sum_cols = ["item_code","item_description","total_qty","total_spend"]
            if show_price_stats:
                sum_cols += ["avg_unit_price","min_unit_price","max_unit_price"]

            # Execute
            cur = conn.execute(sum_sql, params)
            sum_rows = _rows_to_dicts(cur)

            if include_details:
                cur = conn.execute(detail_sql, params)
                det_rows = _rows_to_dicts(cur)
                return _result(sum_cols, sum_rows) | {"details": {"columns": detail_cols, "rows": det_rows}}
            else:
                return _result(sum_cols, sum_rows)

        elif group_by == "project":
            sql = f"""
                SELECT
                    COALESCE(oi.project, o.project) AS project,
                    SUM(oi.qty_ordered) AS total_qty,
                    SUM(oi.total) AS total_spend
                FROM order_items oi
                JOIN orders o ON o.id = oi.order_id
                WHERE {where_clause}
                GROUP BY COALESCE(oi.project, o.project)
                ORDER BY total_spend DESC
            """
            cols = ["project","total_qty","total_spend"]
            cur = conn.execute(sql, params)
            rows = _rows_to_dicts(cur)
            return _result(cols, rows)

        elif group_by == "supplier":
            if group_monthly:
                sql = f"""
                    SELECT
                        s.name AS supplier,
                        strftime('%Y-%m', o.created_date) AS period,
                        SUM(oi.total) AS spend
                    FROM order_items oi
                    JOIN orders o ON o.id = oi.order_id
                    LEFT JOIN suppliers s ON s.id = o.supplier_id
                    WHERE {where_clause}
                    GROUP BY supplier, period
                    ORDER BY supplier, period
                """
                cols = ["supplier","period","spend"]
            else:
                sql = f"""
                    SELECT
                        s.name AS supplier,
                        SUM(oi.total) AS spend
                    FROM order_items oi
                    JOIN orders o ON o.id = oi.order_id
                    LEFT JOIN suppliers s ON s.id = o.supplier_id
                    WHERE {where_clause}
                    GROUP BY supplier
                    ORDER BY spend DESC
                """
                cols = ["supplier","spend"]
            cur = conn.execute(sql, params)
            rows = _rows_to_dicts(cur)
            return _result(cols, rows)

        elif group_by == "requester":
            sql = f"""
                SELECT
                    r.name AS requester,
                    SUM(oi.total) AS spend
                FROM order_items oi
                JOIN orders o ON o.id = oi.order_id
                LEFT JOIN requesters r ON r.id = o.requester_id
                WHERE {where_clause}
                GROUP BY requester
                ORDER BY spend DESC
            """
            cols = ["requester","spend"]
            cur = conn.execute(sql, params)
            rows = _rows_to_dicts(cur)
            return _result(cols, rows)

        elif group_by == "open":
            sql = f"""
                SELECT
                    o.order_number,
                    DATE(o.created_date) AS order_date,
                    s.name AS supplier,
                    r.name AS requester,
                    o.status,
                    SUM(oi.qty_ordered) AS qty_ordered,
                    SUM(oi.total) AS ordered_value
                FROM order_items oi
                JOIN orders o ON o.id = oi.order_id
                LEFT JOIN requesters r ON r.id = o.requester_id
                LEFT JOIN suppliers  s ON s.id = o.supplier_id
                WHERE {where_clause}
                  AND UPPER(o.status) IN ('PENDING','AWAITING AUTHORISATION','AUTHORISED','PARTIALLY RECEIVED')
                GROUP BY o.id
                ORDER BY o.created_date DESC
            """
            cols = ["order_number","order_date","supplier","requester","status","qty_ordered","ordered_value"]
            cur = conn.execute(sql, params)
            rows = _rows_to_dicts(cur)
            return _result(cols, rows)

        elif group_by == "partial":
            sql = f"""
                SELECT
                    o.order_number,
                    DATE(o.created_date) AS order_date,
                    COALESCE(DATE(o.received_date),'') AS received_date,
                    CAST(julianday('now') - julianday(COALESCE(o.received_date, o.created_date)) AS INT) AS days_since_last_event,
                    s.name AS supplier,
                    r.name AS requester
                FROM orders o
                LEFT JOIN requesters r ON r.id = o.requester_id
                LEFT JOIN suppliers  s ON s.id = o.supplier_id
                WHERE {where_clause}
                  AND UPPER(o.status) = 'PARTIALLY RECEIVED'
                ORDER BY days_since_last_event DESC
            """
            cols = ["order_number","order_date","received_date","days_since_last_event","supplier","requester"]
            cur = conn.execute(sql, params)
            rows = _rows_to_dicts(cur)
            return _result(cols, rows)

        elif group_by == "cod":
            sql = f"""
                SELECT
                    o.order_number,
                    DATE(o.created_date) AS order_date,
                    s.name AS supplier,
                    r.name AS requester,
                    o.status,
                    COALESCE(o.payment_terms,'') AS payment_terms,
                    o.total AS order_total
                FROM orders o
                LEFT JOIN requesters r ON r.id = o.requester_id
                LEFT JOIN suppliers  s ON s.id = o.supplier_id
                WHERE {where_clause}
                  AND (UPPER(o.payment_terms)='COD')
                ORDER BY o.created_date DESC
            """
            cols = ["order_number","order_date","supplier","requester","status","payment_terms","order_total"]
            cur = conn.execute(sql, params)
            rows = _rows_to_dicts(cur)
            return _result(cols, rows)

        elif group_by == "variance":
            sql = f"""
                SELECT
                    oi.item_code,
                    oi.item_description,
                    s.name AS supplier,
                    AVG(oi.price) AS avg_price,
                    MIN(oi.price) AS min_price,
                    MAX(oi.price) AS max_price,
                    COUNT(*) AS line_count
                FROM order_items oi
                JOIN orders o ON o.id = oi.order_id
                LEFT JOIN suppliers s ON s.id = o.supplier_id
                WHERE {where_clause}
                GROUP BY oi.item_code, oi.item_description, s.name
                HAVING line_count >= 2
                ORDER BY oi.item_code, avg_price DESC
            """
            cols = ["item_code","item_description","supplier","avg_price","min_price","max_price","line_count"]
            cur = conn.execute(sql, params)
            rows = _rows_to_dicts(cur)
            return _result(cols, rows)

        # Should never reach here due to regex, but be safe
        raise HTTPException(status_code=400, detail="Invalid group_by")
    finally:
        conn.close()

# --- NEW: User Activity report endpoint ---
from typing import Optional, Dict  # (already present? keep only one copy)
from fastapi import Query, Depends  # (already present? keep only one copy)
import sqlite3                     # (already present? keep only one copy)
from backend.database import get_db_connection  # (already present? keep only one copy)
from backend.utils.permissions_utils import require_login  # (already present? keep only one copy)

@router.get("/api/report/user_activity")
async def user_activity_report(
    start_date: Optional[str] = Query(None),
    end_date:   Optional[str] = Query(None),
    requester:  Optional[str] = Query(None),
    supplier:   Optional[str] = Query(None),
    status:     Optional[str] = Query(None),
    exclude_deleted: Optional[bool] = Query(True),
    user: Dict = Depends(require_login),
):
    """
    Returns activity grouped by user based on audit_trail:
      - Actions: total audit entries
      - ActiveDays: distinct days with any action
      - OrdersTouched: distinct orders with any action
      - FirstAction / LastAction: date boundaries
    Filters:
      - start_date/end_date filter by audit_trail.action_date
      - requester/supplier/status filter via joined order metadata
      - exclude_deleted excludes orders with status 'Deleted'
    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        where = []
        params: list = []

        # Dates filter audit_trail timestamps
        if start_date:
            where.append("DATE(at.action_date) >= DATE(?)")
            params.append(start_date)
        if end_date:
            where.append("DATE(at.action_date) <= DATE(?)")
            params.append(end_date)

        # Join-based filters
        if requester and requester.lower() != "all":
            where.append("UPPER(r.name) LIKE UPPER(?)")
            params.append(f"%{requester}%")
        if supplier and supplier.lower() != "all":
            where.append("UPPER(s.name) LIKE UPPER(?)")
            params.append(f"%{supplier}%")
        if status and status.lower() != "all":
            where.append("UPPER(o.status) = UPPER(?)")
            params.append(status)

        if exclude_deleted:
            where.append("UPPER(o.status) <> 'DELETED'")

        where_clause = " AND ".join(where) if where else "1=1"

        sql = f"""
            SELECT
              COALESCE(u.username, '(unknown)')            AS User,
              COUNT(*)                                     AS Actions,
              COUNT(DISTINCT DATE(at.action_date))         AS ActiveDays,
              COUNT(DISTINCT at.order_id)                  AS OrdersTouched,
              MIN(DATE(at.action_date))                    AS FirstAction,
              MAX(DATE(at.action_date))                    AS LastAction
            FROM audit_trail at
            LEFT JOIN users u    ON u.id = at.user_id
            LEFT JOIN orders o   ON o.id = at.order_id
            LEFT JOIN requesters r ON r.id = o.requester_id
            LEFT JOIN suppliers  s ON s.id = o.supplier_id
            WHERE {where_clause}
            GROUP BY COALESCE(u.username, '(unknown)')
            ORDER BY Actions DESC, LastAction DESC
        """
        rows = [dict(row) for row in conn.execute(sql, params).fetchall()]
        return {"columns": ["User", "Actions", "ActiveDays", "OrdersTouched", "FirstAction", "LastAction"],
                "rows": rows}
    finally:
        conn.close()
