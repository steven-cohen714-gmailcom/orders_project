from pathlib import Path

TARGET = Path("backend/endpoints/orders.py")

upload_route = '''
from fastapi import UploadFile, File, Form
import os

@router.post("/upload_attachment")
async def upload_attachment(order_id: int = Form(...), file: UploadFile = File(...)):
    \"""
    Upload an attachment and link it to an order.
    Saves file to data/uploads and logs entry to DB.
    \"""
    import sqlite3
    from datetime import datetime

    # Create upload folder if it doesn't exist
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    filename = file.filename
    filepath = os.path.join(upload_dir, filename)

    # Save file to disk
    with open(filepath, "wb") as f:
        f.write(await file.read())

    # Log in DB
    try:
        conn = sqlite3.connect("data/orders.db")
        cursor = conn.cursor()
        cursor.execute(\"\"\"
            INSERT INTO attachments (
                order_id, filename, file_path, upload_date
            ) VALUES (?, ?, ?, ?)
        \"\"\", (order_id, filename, filepath, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return {"message": "Attachment uploaded", "filename": filename}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
'''

if __name__ == "__main__":
    text = TARGET.read_text()
    insert_point = text.rfind('@router.get')
    updated = text[:insert_point] + upload_route.strip() + '\n\n' + text[insert_point:]
    TARGET.write_text(updated)
    print("✅ /upload_attachment route injected.")
