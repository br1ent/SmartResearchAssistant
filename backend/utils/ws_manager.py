"""WebSocket 连接管理器 + 处理器"""
from typing import Any
from fastapi import WebSocket
from utils.auth import decode_token


class ConnectionManager:
    """管理 WebSocket 连接，支持按 conversation_id 广播"""

    def __init__(self):
        self._connections: dict[int, set[WebSocket]] = {}

    async def connect(self, conversation_id: int, ws: WebSocket):
        await ws.accept()
        self._connections.setdefault(conversation_id, set()).add(ws)

    def disconnect(self, conversation_id: int, ws: WebSocket):
        conns = self._connections.get(conversation_id)
        if conns:
            conns.discard(ws)
            if not conns:
                del self._connections[conversation_id]

    async def broadcast(self, conversation_id: int, data: dict[str, Any]):
        conns = self._connections.get(conversation_id, set())
        dead = set()
        for ws in conns:
            try:
                await ws.send_json(data)
            except Exception:
                dead.add(ws)
        for ws in dead:
            conns.discard(ws)
        if not conns and conversation_id in self._connections:
            del self._connections[conversation_id]

    @property
    def active_connections(self) -> dict[int, int]:
        return {cid: len(conns) for cid, conns in self._connections.items()}


class WsHandler:
    """WebSocket 处理器：验证 → 连接 → 保活(ping/pong)"""

    def __init__(self, manager: ConnectionManager):
        self.manager = manager

    async def handle(self, websocket: WebSocket, conversation_id: int, token:   str  ):
        """验证 token 和对话归属后建立连接，失败则关闭"""
        payload = decode_token(token)
        if payload is None:
            await websocket.close(code=4001, reason="token无效")
            return

        user_id_str = payload.get("sub")
        if not user_id_str:
            await websocket.close(code=4001, reason="token无效")
            return

        # 验证对话归属
        from config.database import SessionLocal
        from models.chat import Conversation
        db = SessionLocal()
        try:
            conv = db.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == int(user_id_str),
            ).first()
            if not conv:
                await websocket.close(code=4003, reason="无权访问该对话")
                return
        finally:
            db.close()

        await self.manager.connect(conversation_id, websocket)
        try:
            while True:
                data = await websocket.receive_text()
                if data == "ping":
                    await websocket.send_json({"type": "pong"})
        except Exception:
            # WebSocketDisconnect 和任何异常都做清理
            pass
        finally:
            self.manager.disconnect(conversation_id, websocket)


manager = ConnectionManager()
ws_handler = WsHandler(manager)
