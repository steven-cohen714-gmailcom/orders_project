from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from backend.database import get_db_connection
from weasyprint import HTML
from io import BytesIO
import logging
import sqlite3

router = APIRouter()

@router.get("/orders/pdf/{order_id}")
async def get_order_pdf(order_id: int):
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT o.*, s.name as supplier_name, r.name as requester_name
                FROM orders o
                LEFT JOIN suppliers s ON o.supplier_id = s.id
                LEFT JOIN requesters r ON o.requester_id = r.id
                WHERE o.id = ?
            """, (order_id,))
            order = cursor.fetchone()
            
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            cursor.execute("""
                SELECT * FROM order_items WHERE order_id = ?
            """, (order_id,))
            items = cursor.fetchall()

        order_dict = dict(order)
        items_list = [dict(item) for item in items]

        logo_path = "file:///Users/stevencohen/Projects/universal_recycling/orders_project/frontend/static/images/universal_logo.jpg"

        html_content = f"""
        <html>
        <head>
            <title>Order {order_dict['order_number']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ text-align: center; }}
                img.logo {{ width: 150px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .vat-note {{ margin-top: 15px; font-style: italic; font-size: 0.9rem; }}
            </style>
        </head>
        <body>
            <img src="{logo_path}" class="logo" />
            <h1>Purchase Order {order_dict['order_number']}</h1>
            <p><strong>Supplier:</strong> {order_dict['supplier_name']}</p>
            <p><strong>Requester:</strong> {order_dict['requester_name']}</p>
            <p><strong>Created Date:</strong> {order_dict['created_date']}</p>
            <p><strong>Total:</strong> R{order_dict['total']}</p>
            <p><strong>Order Note:</strong> {order_dict['order_note'] or 'None'}</p>
            <p><strong>Note to Supplier:</strong> {order_dict['note_to_supplier'] or 'None'}</p>
            <table>
                <tr>
                    <th>Item Code</th>
                    <th>Description</th>
                    <th>Qty Ordered</th>
                    <th>Price</th>
                    <th>Total</th>
                </tr>
        """

        for item in items_list:
            html_content += f"""
                <tr>
                    <td>{item['item_code']}</td>
                    <td>{item['item_description']}</td>
                    <td>{item['qty_ordered']}</td>
                    <td>R{item['price']}</td>
                    <td>R{item['total']}</td>
                </tr>
            """

        html_content += """
            </table>
            <p class="vat-note">All prices exclude VAT.</p>
        </body>
        </html>
        """

        pdf_io = BytesIO()
        HTML(string=html_content).write_pdf(target=pdf_io)
        pdf_io.seek(0)

        logging.info(f"PDF generated for order {order_id}")
        return StreamingResponse(
            pdf_io,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=order_{order_id}.pdf"}
        )

    except Exception as e:
        logging.error(f"PDF generation failed for order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
