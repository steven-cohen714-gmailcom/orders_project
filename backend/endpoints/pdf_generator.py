from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from io import BytesIO
import logging
from datetime import datetime

router = APIRouter()

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
