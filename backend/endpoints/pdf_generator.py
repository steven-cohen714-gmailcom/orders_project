from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from io import BytesIO
import logging
from datetime import datetime
from backend.database import get_db_connection

router = APIRouter(prefix="/orders/api", tags=["pdf"])

@router.post("/generate_pdf")
async def generate_pdf(request: Request):
    try:
        data = await request.json()
        html_content = data.get("html", "<html><body><h1>No Content</h1></body></html>")
        pdf_io = BytesIO()
        HTML(string=html_content).write_pdf(target=pdf_io)
        pdf_io.seek(0)

        logging.info(f"PDF generated at {datetime.now().isoformat()}")
        return StreamingResponse(pdf_io, media_type="application/pdf", headers={
            "Content-Disposition": "inline; filename=generated.pdf"
        })
    except Exception as e:
        logging.error(f"PDF generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="PDF generation failed")

@router.get("/generate_pdf_for_order/{order_id}")
async def generate_pdf_for_order(order_id: int):
    try:
        with get_db_connection() as conn:
            conn.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
            cursor = conn.cursor()

            # Fetch order details
            cursor.execute("""
                SELECT o.*, s.name as supplier, r.name as requester
                FROM orders o
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.id = ?
            """, (order_id,))
            order = cursor.fetchone()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            # Fetch order items
            cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
            items = cursor.fetchall()

            # Fetch business details
            cursor.execute("""
                SELECT company_name, address_line1, address_line2, city, province, postal_code, telephone, vat_number
                FROM business_details WHERE id = 1
            """)
            business_details = cursor.fetchone()
            if not business_details:
                raise HTTPException(status_code=404, detail="Business details not found")

        # Generate HTML for PDF
        html_content = f"""
            <html>
            <head>
                <title>Printable Order - {order['order_number']}</title>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1 {{ text-align: center; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                    th, td {{ border: 1px solid #000; padding: 6px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <h1>Order {order['order_number']}</h1>
                <p><strong>Company:</strong> {business_details['company_name']}</p>
                <p><strong>Address:</strong> {business_details['address_line1']}{', ' + business_details['address_line2'] if business_details['address_line2'] else ''}, {business_details['city']}, {business_details['province']} {business_details['postal_code']}</p>
                <p><strong>Telephone:</strong> {business_details['telephone']}</p>
                <p><strong>VAT Number:</strong> {business_details['vat_number']}</p>
                <p><strong>Status:</strong> {order['status']}</p>
                <p><strong>Created Date:</strong> {order['created_date']}</p>
                <p><strong>Received Date:</strong> {order['received_date'] or "N/A"}</p>
                <p><strong>Total:</strong> R{order['total']}</p>
                <p><strong>Supplier:</strong> {order['supplier'] or "N/A"}</p>
                <p><strong>Requester:</strong> {order['requester']}</p>
                <p><strong>Order Note:</strong> {order['order_note'] or "None"}</p>
                <p><strong>Supplier Note:</strong> {order['note_to_supplier'] or "None"}</p>

                <h2>Line Items</h2>
                <table border="1" cellpadding="6" cellspacing="0">
                    <thead>
                        <tr>
                            <th>Item Code</th>
                            <th>Description</th>
                            <th>Project</th>
                            <th>Qty Ordered</th>
                            <th>Price</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(f'''
                            <tr>
                                <td>{item['item_code']}</td>
                                <td>{item['item_description']}</td>
                                <td>{item['project']}</td>
                                <td>{item['qty_ordered']}</td>
                                <td>R{item['price']}</td>
                                <td>R{item['total']}</td>
                            </tr>
                        ''' for item in items)}
                    </tbody>
                </table>
            </body>
            </html>
        """

        pdf_io = BytesIO()
        HTML(string=html_content).write_pdf(target=pdf_io)
        pdf_io.seek(0)

        logging.info(f"PDF generated for order {order_id} at {datetime.now().isoformat()}")
        return StreamingResponse(pdf_io, media_type="application/pdf", headers={
            "Content-Disposition": f"inline; filename=order_{order_id}.pdf"
        })
    except Exception as e:
        logging.error(f"PDF generation failed for order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")