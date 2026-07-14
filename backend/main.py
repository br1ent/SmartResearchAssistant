from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from config.settings import get_settings
from config.database import engine, Base
from routers.chat import router as chat_router
from routers.chat.reports import router as reports_router
from routers.user import router as user_router
from routers.prompts import router as prompts_router
from routers.ws import router as ws_router

settings = get_settings()

app = FastAPI(
    title="Smart Research Assistant API",
    description="智能研究助手后端API",
    version="1.0.0"
)

# API 路由
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(reports_router)
app.include_router(prompts_router)
app.include_router(ws_router)

# 媒体文件（头像等）
app.mount("/media", StaticFiles(directory="media"), name="media")

# 前端构建产物
FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")


# SPA 兜底：所有未匹配的路径都返回 index.html（Vue Router 接管）
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    return FileResponse(str(FRONTEND_DIST / "index.html"))


@app.get("/favicon.ico")
async def favicon():
    return FileResponse(str(FRONTEND_DIST / "favicon.ico"))


@app.on_event("startup")
def startup():
    """启动时初始化数据库表"""
    import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
