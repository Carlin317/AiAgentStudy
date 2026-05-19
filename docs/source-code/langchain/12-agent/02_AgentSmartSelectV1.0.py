"""
[案例 12-2]多工具并行调用与聚合回答(V1.0:create_agent 一步创建 + 结构化输出)

知识点速览:
- V1.0 不再手写 PromptTemplate/AgentExecutor,改为 create_agent() 一步完成
- response_format 指定 TypedDict,返回中包含 structured_response 字段,便于程序化处理
- create_agent 常见输入:model / tools / system_prompt / response_format
- invoke() 看最终结果;stream() 看中间进展;checkpointer + thread_id 做短期记忆
"""

import os
import json
import httpx
from pathlib import Path
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")


@tool
def get_weather(loc: str) -> str:
    """
    查询即时天气函数
    :param loc: 城市英文名,如 Beijing,Shanghai.
    :return: OpenWeather API 返回的天气信息(JSON 字符串).
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
    return json.dumps(data, ensure_ascii=False)


# ========== 1. 结构化输出定义 ==========
class WeatherCompareOutput(TypedDict):
    beijing_temp: float
    shanghai_temp: float
    hotter_city: str
    summary: str


# ========== 2. 初始化模型 ==========
model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 3. 一步创建 Agent ==========
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt=(
        "你是天气助手."
        "当用户询问多个城市天气时,"
        "你需要分别调用工具获取数据,并进行比较分析."
    ),
    response_format=WeatherCompareOutput,
)

# ========== 4. 调用 ==========
result = agent.invoke({"input": "请问今天北京和上海的天气怎么样,哪个城市更热?"})
print(result)
print()
print(json.dumps(result["structured_response"], ensure_ascii=False, indent=2))

"""
[输出示例]
{
  "beijing_temp": 10.49,
  "shanghai_temp": 15.34,
  "hotter_city": "Shanghai",
  "summary": "上海比北京暖和约4.85度C,且天气晴朗,而北京多云."
}
"""
