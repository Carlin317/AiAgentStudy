"""
[案例 12-1]多工具并行调用与聚合回答(V0.3:Agent + AgentExecutor)

知识点速览:
- Tool 提供能力,Agent 负责决策"何时用,用哪个,如何聚合结果"
- V0.3 流程:model + tools + prompt -> create_tool_calling_agent -> AgentExecutor 执行
- agent_scratchpad 是 Agent 的"草稿区",记录多轮推理与工具输出
- AgentExecutor(verbose=True) 适合教学和排查
"""

import json
import os
import httpx
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

from langchain_classic.agents import create_tool_calling_agent
from langchain_classic.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool


@tool
def get_weather(loc):
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
    print(json.dumps(data))
    return json.dumps(data)


# ========== 1. 初始化大模型 ==========
llm = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 2. 对话结构 ==========
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是天气助手,请根据用户的问题,给出相应的天气信息"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

tools = [get_weather]

# ========== 3. 组装 Agent ==========
agent = create_tool_calling_agent(llm, tools, prompt)

# ========== 4. AgentExecutor 驱动循环 ==========
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke(
    {"input": "请问今天北京和上海的天气怎么样,哪个城市更热?"}
)

print(result)
