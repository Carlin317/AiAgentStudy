"""
【案例 08-4】天气查询工具：将第三方 HTTP API 封装为可被 LLM 调用的 Tool

对应教程章节：第 17 章 - Tools 工具调用 → 5、天气助手实战 → 5.2 定义天气查询工具

知识点速览：
- 将第三方 API 封装为 Tool 的关键：docstring 写清调用场景和参数约束
- loc 参数需传英文城市名（如 Beijing）等约束应直接写在工具说明中
- 返回 JSON 字符串便于后续链路继续处理
"""

from langchain_core.tools import tool
import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")


# ========== 1. 工具定义 ==========
@tool
def get_weather(loc: str) -> str:
    """
    查询指定城市的即时天气。

    参数:
        loc: 城市名称字符串。建议优先传英文城市名，如 Beijing、Shanghai。

    返回:
        OpenWeather 当前天气接口返回的 JSON 字符串。
    """
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": loc,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric",
        "lang": "zh_cn",
    }

    response = httpx.get(url, params=params, timeout=30)

    data = response.json()
    return json.dumps(data)


# ========== 2. 本地测试 ==========
result = get_weather.invoke("beijing")
print(result)
