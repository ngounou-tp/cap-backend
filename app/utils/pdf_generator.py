from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from fastapi.responses import StreamingResponse
from app.models.issuance import ShareIssuance 
from app.models.shareholder import ShareholderProfile

def generate_certificate(issuance: ShareIssuance, shareholder: ShareholderProfile):
    print(issuance)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, 750, "Share Certificate")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Certificate for: {shareholder.name}")
    c.drawString(100, 680, f"Email: {shareholder.user.email}")  # fixed here
    c.drawString(100, 660, f"Number of Shares: {issuance.number_of_shares}")
    c.drawString(100, 640, f"Issuance Date: {issuance.date.strftime('%Y-%m-%d')}")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
