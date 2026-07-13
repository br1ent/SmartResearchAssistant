"""闲聊 LLM 节点：直接调用 DeepSeek 返回回复"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from config.agents import get_agent_settings
from config.prompts import get_chat_system_prompt

settings = get_agent_settings()

llm = ChatOpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url=settings.DEEPSEEK_BASE_URL,
    model=settings.DEEPSEEK_MODEL,
    temperature=settings.DEEPSEEK_TEMPERATURE,
    max_tokens=settings.DEEPSEEK_MAX_TOKENS,
)


def chat_node(state: dict) -> dict:
    """闲聊节点：构建消息列表 → 调 DeepSeek → 返回回复"""
    system_prompt = get_chat_system_prompt()
    messages = [SystemMessage(content=system_prompt)]

    for msg in state.get("history", []):
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    # 加上当前用户消息
    messages.append(HumanMessage(content=state["user_message"]))

    response = llm.invoke(messages)
    return {"reply": response.content}
