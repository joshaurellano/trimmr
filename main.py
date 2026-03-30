from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from secrets import token_urlsafe
from pydantic import BaseModel
from supabase import create_client, Client
from typing import Optional
from PIL import Image
from dotenv import load_dotenv

import qrcode
import io
import os
import json
import validators

app = FastAPI()

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Url(BaseModel):
    url : str

@app.get('/')
def home():
    return {'msg': 'Root'}

@app.post("/generate")
async def generate_qr_code(url: Url):
    try:
        img = qrcode.make(url.url)
        filename = "qrcode.png"

        output_buffer = io.BytesIO()
        img.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return StreamingResponse(output_buffer, media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@app.post('/short_url')
def short_url(url : Url):
    if validators.url(url.url):
        url_id = token_urlsafe(5)
        shorted_url = f'http://127.0.0.1:8000/{url_id}'
        supabase.table('urls').insert({
        'url_id': url_id,
        'short_url': shorted_url,
        'target_url': url.url
    }).execute()

        return {'msg': 'done', 'url': shorted_url}

    return {'msg': 'Invalled url'}


@app.get('/{_id}')
def get_target_url(_id: str):
    result = supabase.table('urls').select('target_url').eq('url_id', _id).execute()

    if result.data:
        return RedirectResponse(result.data[0]['target_url'])
    
    raise HTTPException(
        status_code=404,
        detail="URL not found"
    )