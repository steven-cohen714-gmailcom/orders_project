from fastapi import APIRouter, HTTPException, UploadFile, Form
from datetime import datetime
import sqlite3
from pathlib import Path
import json  # Add this import

router = APIRouter(tags=["orders"])

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def log_event(filename: str, data: dict):
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

# Rest of the file remains unchanged
@router.post("/upload_attachment")
async def upload_attachment(file: UploadFile, order_id: int = Form(...)):
    try:
        # Validate order_id exists
        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=400, detail="Invalid order_id")

        # Sanitize filename and handle duplicates
        filename = file.filename.replace(" ", "_").replace("/", "_").replace("\\", "_")
        base_filename = filename
        saved_path = UPLOAD_DIR / f"{order_id}_{filename}"
        counter = 1
        while saved_path.exists():
            name, ext = base_filename.rsplit(".", 1) if "." in base_filename else (base_filename, "")
            filename = f"{name}_{counter}.{ext}" if ext else f"{name}_{counter}"
            saved_path = UPLOAD_DIR / f"{order_id}_{filename}"
            counter += 1

        # Check file size before saving
        content = await file.read()
        file_size = len(content)
        if file_size < 500:
            raise HTTPException(status_code=400, detail="Uploaded file is too small or corrupt.")

        # Save the file
        with saved_path.open("wb") as buffer:
            buffer.write(content)

        with sqlite3.connect("data/orders.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attachments (order_id, filename, file_path, upload_date)
                VALUES (?, ?, ?, ?)
            """, (order_id, filename, str(saved_path), datetime.now().isoformat()))
            conn.commit()

        log_event("new_orders_log.txt", {
            "action": "attachment_uploaded",
            "order_id": order_id,
            "filename": filename,
            "path": str(saved_path),
            "size_bytes": file_size
        })

        return {"status": "✅ Attachment uploaded"}
    except sqlite3.Error as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "sqlite_upload"})
        raise HTTPException(status_code=500, detail=f"Database error during upload: {str(e)}")
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "upload"})
        raise HTTPException(status_code=500, detail=f"Failed to upload attachment: {str(e)}")
    finally:
        await file.close()

@router.get("/attachments/{order_id}")
def get_order_attachments(order_id: int):
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, filename, file_path, upload_date
                FROM attachments
                WHERE order_id = ?
            """, (order_id,))
            files = [dict(row) for row in cursor.fetchall()]
        return {"attachments": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve attachments: {e}")