from fastapi import APIRouter
from models.models import Url
from config.database import supabase

from controllers.urlsController import short_url, get_target_url

router = APIRouter()

@router.post("/short")
async def short_url_route(url: Url):
    return await short_url(url)

@router.get("/{_id}")
async def get_target_url_route(_id: str):
    return await get_target_url(_id)