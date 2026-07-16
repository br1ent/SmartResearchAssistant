"""Agent 工具：时间、天气、搜索"""
from datetime import datetime, timezone, timedelta

import httpx
from langchain_core.tools import tool
from langchain_tavily import TavilySearch

from config.agents import get_agent_settings

settings = get_agent_settings()

# 中国时区 UTC+8
_CN_TZ = timezone(timedelta(hours=8))


@tool
def get_current_time() -> str:
    """获取当前中国时间（北京时间）。当用户询问时间、日期、今天几号等问题时使用。"""
    return datetime.now(_CN_TZ).strftime("%Y-%m-%d %H:%M:%S")


# 常见中文城市名 → 英文名映射
_CITY_MAP = {
    "北京": "Beijing", "上海": "Shanghai", "广州": "Guangzhou", "深圳": "Shenzhen",
    "杭州": "Hangzhou", "南京": "Nanjing", "成都": "Chengdu", "重庆": "Chongqing",
    "武汉": "Wuhan", "西安": "Xian", "天津": "Tianjin", "苏州": "Suzhou",
    "长沙": "Changsha", "郑州": "Zhengzhou", "东莞": "Dongguan", "青岛": "Qingdao",
    "沈阳": "Shenyang", "宁波": "Ningbo", "昆明": "Kunming", "大连": "Dalian",
    "厦门": "Xiamen", "哈尔滨": "Harbin", "济南": "Jinan", "福州": "Fuzhou",
    "佛山": "Foshan", "长春": "Changchun", "温州": "Wenzhou", "石家庄": "Shijiazhuang",
    "南宁": "Nanning", "常州": "Changzhou", "泉州": "Quanzhou", "南昌": "Nanchang",
    "贵阳": "Guiyang", "太原": "Taiyuan", "烟台": "Yantai", "嘉兴": "Jiaxing",
    "南通": "Nantong", "金华": "Jinhua", "珠海": "Zhuhai", "惠州": "Huizhou",
    "徐州": "Xuzhou", "海口": "Haikou", "乌鲁木齐": "Urumqi", "绍兴": "Shaoxing",
    "中山": "Zhongshan", "台州": "Taizhou", "兰州": "Lanzhou", "潍坊": "Weifang",
    "保定": "Baoding", "镇江": "Zhenjiang", "扬州": "Yangzhou", "桂林": "Guilin",
    "唐山": "Tangshan", "三亚": "Sanya", "湖州": "Huzhou", "呼和浩特": "Hohhot",
    "廊坊": "Langfang", "洛阳": "Luoyang", "威海": "Weihai", "盐城": "Yancheng",
}


@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气。当用户询问某地天气、温度、是否下雨等问题时使用。

    Args:
        city: 城市名称，支持中文如"北京"，或英文如"Beijing"
    """
    try:
        # 中文城市名转英文
        query_city = _CITY_MAP.get(city, city)
        resp = httpx.get(
            f"https://wttr.in/{query_city}",
            params={"format": "j1", "lang": "zh"},
            timeout=10.0,
        )
        resp.raise_for_status()
        data = resp.json()
        current = data["current_condition"][0]
        desc = current["weatherDesc"][0]["value"]
        temp = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        wind = current["windspeedKmph"]
        return (
            f"{city}天气：{desc}\n"
            f"温度：{temp}°C（体感 {feels_like}°C）\n"
            f"湿度：{humidity}%\n"
            f"风速：{wind} km/h"
        )
    except Exception as e:
        return f"天气查询失败：{e}"


@tool
def web_search(query: str) -> str:
    """联网搜索获取最新信息。当用户询问新闻、实时信息、需要最新数据的问题时使用。

    Args:
        query: 搜索关键词
    """
    try:
        tool = TavilySearch(
            tavily_api_key=settings.TAVILY_API_KEY,
            max_results=3,
        )
        results = tool.invoke({"query": query})
        lines = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "无标题")
            url = r.get("url", "")
            content = r.get("content", "")[:300]
            lines.append(f"{i}. **{title}**\n   {url}\n   {content}")
        return "\n\n".join(lines) if lines else "未找到相关结果"
    except Exception as e:
        return f"搜索失败：{e}"


CHAT_TOOLS = [get_current_time, get_weather, web_search]
