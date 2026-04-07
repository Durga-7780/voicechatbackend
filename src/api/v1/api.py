from fastapi import APIRouter
from src.api.v1.endpoints import chat, voice, rest

api_router = APIRouter()
api_router.include_router(rest.router, prefix="/rest", tags=["rest"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(voice.router, prefix="/rtc", tags=["rtc"])
