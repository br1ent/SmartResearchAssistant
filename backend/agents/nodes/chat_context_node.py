"""闲聊上下文组装节点：从 DB 读取历史、记忆、提示词，组装 LLM 消息列表"""
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from agents.chat_state import ChatState
from config.prompts import get_chat_system_prompt
from config.database import SessionLocal


def build_context_node(state: ChatState) -> dict:
    """组装闲聊 LLM 所需的完整上下文"""
    conversation_id = state["conversation_id"]
    user_id = state["user_id"]

    # 1. 系统提示词
    system_prompt = get_chat_system_prompt()

    # 2. 用户记忆
    memory_text = ""
    if user_id:
        db = SessionLocal()
        try:
            from models.user import User
            user = db.query(User).filter(User.id == user_id).first()
            if user and user.memory:
                memory_text = user.memory
        finally:
            db.close()

    # 3. 历史消息
    db = SessionLocal()
    try:
        from services.chat.conversation_service import ConversationService
        conv_service = ConversationService(db)
        history = conv_service.get_messages(conversation_id, limit=20)
        history_dicts = [{"role": m.role, "content": m.content} for m in history]
    finally:
        db.close()

    # 4. 组装完整消息列表
    messages = [SystemMessage(content=system_prompt)]
    if memory_text:
        messages.append(SystemMessage(content=f"[用户画像]\n{memory_text}"))

    # 历史消息（跳过最后一条，因为它是刚存入的 user_message，后面会单独加）
    for msg in history_dicts[:-1]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    # 当前用户消息
    messages.append(HumanMessage(content=state["user_message"]))

    return {
        "system_prompt": system_prompt,
        "memory_text": memory_text,
        "history": history_dicts,
        "messages": messages,
    }
