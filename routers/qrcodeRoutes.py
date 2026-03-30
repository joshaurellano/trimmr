from fastapi import APIRouter
from models.models import Url

from controllers.qrcodeController import generate_qr_code

router = APIRouter(prefix="/qrcode", tags=["QR Code"])

@router.post("/generate")
async def generate_qr_code_route(url: Url):
    return await generate_qr_code(url)
    