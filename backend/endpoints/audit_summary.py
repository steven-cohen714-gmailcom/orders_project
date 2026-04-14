# File: backend/endpoints/audit_summary.py
from fastapi import APIRouter, HTTPException, Depends
from backend.database import get_db_connection
from backend.utils.permissions_utils import require_login
import sqlite3

router = APIRouter(tags=["audit_summary"])

# IMPORTANT
# main.py must include this router with prefix="/orders":
#   from backend.endpoints import audit_summary
#   app.include_router(audit_summary.router, prefix="/orders")

@router.get("/api/audit_summary")
def audit_summary(
    start_date: str | None = None,
    end_date: str | None = None,
    requester: str | None = None,
    supplier: str | None = None,
    status: str | None = None,
    order_number: str | None = None,
    include_deleted: int = 0,
    _: bool = Depends(require_login),
):
    """
    One row per order_number:
      - latest_status, supplier, requester, total (from latest non-Deleted header)
      - latest_order_id (for Actions / expand)
      - created_at  : earliest activity for this order_number
      - edited_at   : latest of {'Converted to Draft','Draft Updated'}
      - finalised_at: latest of {'Submitted for Review'}
    Filters apply to the latest header row (except order_number which is exact).
    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    where_latest = []
    params = []

    # Filters apply to "latest" header row
    if status and status.lower() != "all":
        where_latest.append("l.status = ?")
        params.append(status)
    if requester and requester.lower() != "all":
        where_latest.append("r.name = ?")
        params.append(requester)
    if supplier and supplier.lower() != "all":
        where_latest.append("s.name = ?")
        params.append(supplier)
    if start_date:
        where_latest.append("l.created_date >= ?")
        params.append(f"{start_date} 00:00:00")
    if end_date:
        where_latest.append("l.created_date <= ?")
        params.append(f"{end_date} 23:59:59")
    if order_number:
        where_latest.append("l.order_number = ?")
        params.append(order_number)

    # Exclude Deleted by default for the LATEST header choice
    deleted_clause = "" if include_deleted else "WHERE status <> 'Deleted'"

    # Build SQL
    sql = f"""
WITH latest AS (
  SELECT o.*
  FROM orders o
  JOIN (
    SELECT order_number, MAX(id) AS max_id
    FROM orders
    {deleted_clause}
    GROUP BY order_number
  ) m ON m.order_number = o.order_number AND m.max_id = o.id
),
events AS (
  SELECT
    o.order_number,
    MIN(COALESCE(at.action_date, o.created_date)) AS created_at,
    MAX(CASE WHEN at.action IN ('Converted to Draft','Draft Updated')
             THEN at.action_date END)             AS edited_at,
    MAX(CASE WHEN at.action IN ('Submitted for Review')
             THEN at.action_date END)             AS finalised_at
  FROM orders o
  LEFT JOIN audit_trail at ON at.order_id = o.id
  GROUP BY o.order_number
)
SELECT
  l.id               AS latest_order_id,
  l.order_number,
  l.status           AS latest_status,
  l.total,
  l.created_date     AS latest_created_date,
  s.name             AS supplier,
  r.name             AS requester,
  e.created_at,
  e.edited_at,
  e.finalised_at
FROM latest l
LEFT JOIN suppliers s ON s.id = l.supplier_id
LEFT JOIN requesters r ON r.id = l.requester_id
LEFT JOIN events e     ON e.order_number = l.order_number
"""

    if where_latest:
        sql += " WHERE " + " AND ".join(where_latest)

    sql += """
    ORDER BY COALESCE(e.created_at, l.created_date) DESC,
            CASE
            WHEN l.order_number GLOB '*[0-9]*'
                THEN CAST(REPLACE(REPLACE(REPLACE(l.order_number,'UPO',''),'PO',''),'REQ','') AS INTEGER)
            ELSE NULL
            END DESC,
            l.order_number DESC
    """

    try:
        cur.execute(sql, params)
        rows = [dict(row) for row in cur.fetchall()]
        return {"orders": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build audit summary: {e}")
    finally:
        conn.close()
