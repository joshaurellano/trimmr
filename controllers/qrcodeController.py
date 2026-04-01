from fastapi.responses import StreamingResponse
from fastapi import HTTPException
import qrcode
import io

from models.models import Url
from utils.validator import urlValidator

async def generate_qr_code(url:Url):

    validator, normalized_url = await urlValidator(url.url)

    if not validator:
        raise HTTPException(status_code=400, detail="Invalid URL")
    
    try:
        img = qrcode.make(normalized_url)
        output_buffer = io.BytesIO()
        img.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        return StreamingResponse(output_buffer, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")