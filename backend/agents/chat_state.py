"""闲聊模式 LangGraph 状态定义"""
from typing import TypedDict, List
from langchain_core.messages import BaseMessage


class ChatState(TypedDict):
    """闲聊图的共享状态"""
    conversation_id: int
    user_message: str
    user_id: int
    # 上下文组件
    system_prompt: str
    memory_text: str
    history: List[dict]
    # 组装后的完整消息列表
    messages: List[BaseMessage]
