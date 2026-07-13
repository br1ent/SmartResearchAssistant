"""闲聊 LangGraph：START → chat_node → END"""
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from agents.nodes.chat_node import chat_node


class ChatState(TypedDict):
    conversation_id: int
    user_message: str
    history: List[dict]  # [{role, content}]
    reply: str


class ChatGraph:
    """最简闲聊图：一个 LLM 节点完成对话"""

    def __init__(self):
        builder = StateGraph(ChatState)
        builder.add_node("chat_llm", chat_node)
        builder.add_edge("chat_llm", END)
        builder.set_entry_point("chat_llm")
        self.compiled = builder.compile()

    def invoke(self, state: ChatState) -> ChatState:
        return self.compiled.invoke(state)

    async def ainvoke(self, state: ChatState) -> ChatState:
        return await self.compiled.ainvoke(state)
