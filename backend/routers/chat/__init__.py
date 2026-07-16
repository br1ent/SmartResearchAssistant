"""Chat 路由聚合"""
from fastapi import APIRouter
from routers.chat.conversations import router as conv_router
from routers.chat.stream import router as stream_router

router = APIRouter()
router.include_router(conv_router)
router.include_router(stream_router)
