# File: backend/endpoints/requisitions.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse # Keep FileResponse if it's used for other non-requisition PDFs
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sqlite3
from pathlib import Path
import traceback
import logging # Ensure logging is imported if used directly here

router = APIRouter(tags=["requisitions"])

DB_PATH = Path("data/orders.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- Models ---------------- #

class RequisitionItem(BaseModel):
    description: str
    quantity: float
    project: Optional[str] = None 

class RequisitionPayload(BaseModel):
    requisition_number: str
    requisitioner_id: int
    requisition_note: str
    items: List[RequisitionItem]

# ---------------- Endpoint ---------------- #

@router.post("/requisitions", response_model=dict)
async def submit_requisition(payload: RequisitionPayload):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Step 1: check if requisition_number already exists
            cursor.execute(
                "SELECT 1 FROM requisitions WHERE requisition_number = ?",
                (payload.requisition_number,)
            )
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Requisition number already exists")

            # Step 2: insert new requisition
            cursor.execute("""
                INSERT INTO requisitions (
                    requisition_number,
                    requisitioner_id,
                    requisition_note,
                    requisition_date,
                    status
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                payload.requisition_number,
                payload.requisitioner_id,
                payload.requisition_note,
                datetime.now().isoformat(timespec='seconds'), 
                "submitted"
            ))

            requisition_id = cursor.lastrowid

            for item in payload.items:
                cursor.execute("""
                    INSERT INTO requisition_items (
                        requisition_id,
                        description,
                        quantity,
                        project 
                    ) VALUES (?, ?, ?, ?)
                """, (
                    requisition_id,
                    item.description,
                    item.quantity,
                    item.project 
                ))

            # Step 3: update settings to bump requisition_number_start
            # Use the dedicated function from backend.database, which handles the logic and update
            from backend.database import get_next_requisition_number 
            get_next_requisition_number() 

            # Step 4: relink temporary attachments
            cursor.execute("""
                UPDATE requisition_attachments 
                SET requisition_id = ?, requisition_number = NULL
                WHERE requisition_id IS NULL AND requisition_number = ?
            """, (
                requisition_id,
                payload.requisition_number 
            ))

            conn.commit()
            return {"status": "success", "requisition_id": requisition_id}

    except HTTPException as he:
        raise he  
    except Exception as e:
        logging.error("🔥 Backend crash in submit_requisition:", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error submitting requisition: {str(e)}")

@router.get("/api/pending_requisitions", response_model=dict)
async def get_pending_requisitions(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    requisitioner: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            filters = []
            params = []

            valid_statuses = ["submitted", "ordered", "converted", "pending", "declined"] 
            if status and status.lower() != "all":
                if status.lower() in valid_statuses:
                    filters.append("LOWER(r.status) = LOWER(?)")
                    params.append(status)
                else:
                    filters.append("LOWER(r.status) = LOWER(?)")
                    params.append(status)
            else:
                filters.append("LOWER(r.status) IN ('submitted', 'ordered')") 

            if start_date:
                try:
                    datetime.strptime(start_date, "%Y-%m-%d")
                    filters.append("DATE(r.requisition_date) >= DATE(?)")
                    params.append(start_date)
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")

            if end_date:
                try:
                    datetime.strptime(end_date, "%Y-%m-%d")
                    filters.append("DATE(r.requisition_date) <= DATE(?)")
                    params.append(end_date)
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD.")

            if requisitioner and requisitioner.lower() != "all":
                filters.append("LOWER(rq.name) LIKE LOWER(?)")
                params.append(f"%{requisitioner}%")
            
            where_clause = " AND ".join(filters) if filters else "1=1"

            cursor.execute(f"""
                SELECT
                    r.id,
                    r.requisition_number,
                    r.requisition_date,
                    r.requisition_note,
                    r.status,
                    r.converted_order_id,
                    rq.name AS requisitioner,
                    (
                        SELECT GROUP_CONCAT(ri.description || ' (Qty: ' || ri.quantity || ')' || CASE WHEN ri.project IS NOT NULL AND ri.project != '' THEN ' [Prj: ' || ri.project || ']' ELSE '' END, '; ')
                        FROM requisition_items ri
                        WHERE ri.requisition_id = r.id
                    ) AS description,
                    (
                        SELECT SUM(ri.quantity)
                        FROM requisition_items ri
                        WHERE ri.requisition_id = r.id
                    ) AS total_quantity
                FROM requisitions r
                LEFT JOIN requisitioners rq ON r.requisitioner_id = rq.id
                WHERE {where_clause}
                ORDER BY r.requisition_date DESC
            """, params)

            rows = cursor.fetchall()
            requisitions = [dict(row) for row in rows]

            # MODIFIED: Robust date parsing for display on frontend
            for req in requisitions:
                if req["requisition_date"]:
                    date_str = req["requisition_date"]
                    formatted_date = "N/A"
                    try:
                        formatted_date = datetime.fromisoformat(date_str).strftime("%Y-%m-%d")
                    except ValueError:
                        try:
                            formatted_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")
                        except ValueError:
                            try:
                                formatted_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                            except ValueError:
                                try:
                                    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
                                except ValueError:
                                    logging.warning(f"Could not parse date for requisition {req['id']}: {date_str}")
                    req["requisition_date"] = formatted_date
                else:
                    req["requisition_date"] = "N/A"

            return {"requisitions": requisitions}

    except Exception as e:
        logging.error(f"Error fetching requisitions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching requisitions: {str(e)}")

@router.get("/api/requisition_items/{requisition_id}")
def get_requisition_items(requisition_id: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    id,
                    description AS item_description,
                    quantity AS qty_ordered,
                    project, 
                    '-' AS item_code,
                    0 AS price,
                    0 AS total
                FROM requisition_items
                WHERE requisition_id = ?
            """, (requisition_id,))
            items = [dict(row) for row in cursor.fetchall()]
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch requisition items: {str(e)}")

# --- REMOVED: requisition_pdf endpoint as it's not desired for requisitions ---
# @router.get("/requisitions/api/generate_pdf/{requisition_id}")
# def requisition_pdf(requisition_id: int):
#    # ... (removed code) ...
# --- END REMOVED ---
    
@router.put("/requisitions/api/mark_converted/{requisition_id}") 
def mark_requisition_converted(requisition_id: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM requisitions WHERE id = ?", (requisition_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Requisition not found")

            # --- CRITICAL FIX: Correct converted_order_id update ---
            # Your .schema output shows converted_order_id as INTEGER.
            # It CANNOT be updated with a string like 'ORDER-CONVERTED'.
            # If you want to link it to an order, you need the actual order ID (an integer).
            # If you just want to flag it as 'converted', use the 'status' column.
            # Assuming 'ordered' status is used for 'converted' state.
            cursor.execute("""
                UPDATE requisitions
                SET status = 'ordered', converted_order_id = NULL -- Set to NULL if no actual order ID
                WHERE id = ?
            """, (requisition_id,))
            
            conn.commit()

        return {"success": True, "message": "Requisition marked as converted and status updated to 'ordered'."}
    except Exception as e:
        logging.error(f"Error marking requisition converted: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to mark converted: {str(e)}")