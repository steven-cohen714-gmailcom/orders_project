from fastapi import APIRouter, HTTPException
from backend.database import get_db_connection
import logging

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

        html_content = f"""
        <html>
        <head>
            <title>Order {order_dict['order_number']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
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
                    <th>Project</th>
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
                    <td>{item['project']}</td>
                    <td>{item['qty_ordered']}</td>
                    <td>R{item['price']}</td>
                    <td>R{item['total']}</td>
                </tr>
            """

        html_content += """
            </table>
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