"""闲聊 LangGraph：START → build_context → END"""
from langgraph.graph import StateGraph, END

from agents.chat_state import ChatState
from agents.nodes.chat_context_node import build_context_node


class ChatGraph:
    """闲聊上下文组装图：从 DB 构建完整的 LLM 消息列表"""

    def __init__(self):
        builder = StateGraph(ChatState)
        builder.add_node("build_context", build_context_node)
        builder.set_entry_point("build_context")
        builder.add_edge("build_context", END)
        self.compiled = builder.compile()

    def invoke(self, state: ChatState) -> ChatState:
        return self.compiled.invoke(state)
