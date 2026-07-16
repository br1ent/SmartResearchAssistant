"""闲聊 LangGraph：START → build_context → END（工具循环由 service 层协调）"""
from langgraph.graph import StateGraph, END

from agents.chat_state import ChatState
from agents.nodes.chat_context_node import build_context_node


class ChatGraph:
    """闲聊图：上下文组装（ReAct 循环由 service 层驱动）"""

    def __init__(self):
        builder = StateGraph(ChatState)
        builder.add_node("build_context", build_context_node)
        builder.set_entry_point("build_context")
        builder.add_edge("build_context", END)
        self.compiled = builder.compile()

    def invoke(self, state: ChatState) -> ChatState:
        return self.compiled.invoke(state)
