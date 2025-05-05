from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from fastapi.responses import FileResponse
import time
from typing import Optional, List
import json

router = APIRouter(prefix="/orders", tags=["orders"])

PDF_DIR = Path("data/pdfs")
PDF_DIR.mkdir(parents=True, exist_ok=True)

def log_event(filename: str, data: dict):
    log_path = Path(f"logs/{filename}")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")

class OrderPDF(BaseModel):
    order_number: str
    date: str
    supplier_id: int
    note_to_supplier: Optional[str]
    items: List[dict]
    total: float
    business_details: dict

@router.post("/generate_pdf")
def generate_pdf(order: OrderPDF):
    start_time = time.time()
    try:
        with sqlite3.connect("data/orders.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, address_line1, address_line2, address_line3, postal_code
                FROM suppliers
                WHERE id = ?
            """, (order.supplier_id,))
            supplier = cursor.fetchone()
            if not supplier:
                raise HTTPException(status_code=404, detail="Supplier not found")
            supplier_dict = dict(supplier)

        pdf_path = PDF_DIR / f"order_{order.order_number}.pdf"
        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 50, order.business_details.get("company_name", "Universal Recycling Company Pty Ltd"))
        c.setFont("Helvetica", 10)
        y = height - 65
        c.drawString(50, y, order.business_details.get("address_line1", ""))
        if order.business_details.get("address_line2"):
            y -= 15
            c.drawString(50, y, order.business_details.get("address_line2", ""))
        y -= 15
        c.drawString(50, y, f"{order.business_details.get('city', '')}, {order.business_details.get('province', '')} {order.business_details.get('postal_code', '')}")
        y -= 15
        c.drawString(50, y, f"Telephone: {order.business_details.get('telephone', '')}")
        y -= 15
        c.drawString(50, y, f"VAT Number: {order.business_details.get('vat_number', '')}")

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 150, f"Purchase Order {order.order_number}")

        c.setFont("Helvetica", 10)
        y = height - 180
        c.drawString(50, y, f"Order Date: {order.date}")
        y -= 15
        c.drawString(50, y, f"Supplier: {supplier_dict['name']}")
        y -= 15
        supplier_address = ", ".join(filter(None, [
            supplier_dict.get("address_line1", ""),
            supplier_dict.get("address_line2", ""),
            supplier_dict.get("address_line3", ""),
            supplier_dict.get("postal_code", "")
        ]))
        c.drawString(50, y, f"Supplier Address: {supplier_address}")

        y -= 40
        c.setFont("Helvetica-Bold", 10)
        headers = ["Stock Code", "Description", "Qty", "Unit Price", "Total"]
        x_positions = [50, 130, 330, 420, 500]
        for i, header in enumerate(headers):
            c.drawString(x_positions[i], y, header)
        y -= 5
        c.line(50, y, width - 50, y)

        c.setFont("Helvetica", 10)
        y -= 15
        for item in order.items:
            c.drawString(x_positions[0], y, item["item_code"])
            c.drawString(x_positions[1], y, item["item_description"][:40])
            c.drawString(x_positions[2], y, str(item["qty_ordered"]))
            c.drawString(x_positions[3], y, f"R{item['price']:.2f}")
            c.drawString(x_positions[4], y, f"R{(item['qty_ordered'] * item['price']):.2f}")
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50

        y -= 20
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"Total (Excluding Tax): R{order.total:.2f}")

        if order.note_to_supplier:
            y -= 20
            c.setFont("Helvetica", 10)
            text = c.beginText(50, y)
            lines = order.note_to_supplier.splitlines()
            text.textLine("Note to Supplier:")
            for line in lines:
                text.textLine(line)
            c.drawText(text)
            y -= 12 * (len(lines) + 1)

        # ✅ Bottom date intentionally removed

        c.showPage()
        c.save()

        end_time = time.time()
        log_event("pdf_generation_log.txt", {
            "action": "pdf_generated",
            "order_number": order.order_number,
            "time_taken_ms": (end_time - start_time) * 1000
        })

        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"order_{order.order_number}.pdf"
        )
    except Exception as e:
        log_event("new_orders_log.txt", {"error": str(e), "type": "generate_pdf"})
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")
