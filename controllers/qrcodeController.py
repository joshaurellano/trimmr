from fastapi.responses import StreamingResponse
from fastapi import HTTPException
import qrcode
import io

from models.models import Url

async def generate_qr_code(url:Url):

    try:
        img = qrcode.make(url.url)
        output_buffer = io.BytesIO()
        img.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        return StreamingResponse(output_buffer, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")