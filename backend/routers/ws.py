"""WebSocket 路由"""
from fastapi import APIRouter, WebSocket, Query
from utils.ws_manager import ws_handler

router = APIRouter()


@router.websocket("/ws/{conversation_id}")
async def ws_endpoint(websocket: WebSocket, conversation_id: int, token:   str   = Query(...)):
    await ws_handler.handle(websocket, conversation_id, token)
