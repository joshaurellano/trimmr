from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from secrets import token_urlsafe
import os

from config.database import supabase
from models.models import Url
from utils.validator import urlValidator

BASE_URL = os.getenv("BASE_URL")

async def short_url(url: Url):
    
    validator, normalized_url = await urlValidator(url.url)

    if not validator:
        raise HTTPException(status_code=400, detail="Invalid URL")

    url_id = token_urlsafe(5)
    shorted_url = f'{BASE_URL}{url_id}'

    supabase.table('urls').insert({
        'url_id': url_id,
        'short_url': shorted_url,
        'target_url': normalized_url
    }).execute()

    return {
        'msg': 'done', 
        'url': shorted_url}

async def get_target_url(_id: str):
    result = supabase.table('urls').select('target_url').eq('url_id', _id).execute()

    if result.data:
        return RedirectResponse(result.data[0]['target_url'])

    raise HTTPException(status_code=404, detail="URL not found")