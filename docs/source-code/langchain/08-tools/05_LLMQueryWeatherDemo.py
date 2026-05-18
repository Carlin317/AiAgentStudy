"""
【案例 08-5】天气助手完整链路：bind_tools → 解析 tool_calls → 执行工具 → 模型转述

对应教程章节：第 17 章 - Tools 工具调用 → 5、天气助手实战 → 5.4 完整链路 / 5.5 与官方主线的关系

知识点速览：
- bind_tools() 将工具声明给模型，模型判断需要时才返回 tool_calls
- 链路三阶段：参数生成（模型）→ 工具执行（程序）→ 结果转述（模型）
- 本例采用课程入门写法，与官方 AIMessage.tool_calls → ToolMessage 主线本质相同
"""

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

import os
from langchain_core.output_parsers import JsonOutputKeyToolsParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from loguru import logger
from QueryWeatherTool import get_weather

# ========== 1. 初始化模型并绑定工具 ==========
llm = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

llm_with_tools = llm.bind_tools([get_weather])

# ========== 2. 天气查询链 ==========
# 从模型输出中提取工具参数 → 执行 get_weather → 得到天气 JSON
parser = JsonOutputKeyToolsParser(key_name=get_weather.name, first_tool_only=True)
get_weather_chain = llm_with_tools | parser | get_weather

# ========== 3. 输出链：将天气 JSON 转为自然语言描述 ==========
output_prompt = PromptTemplate.from_template(
    """你将收到一段 JSON 格式的天气数据{weather_json}，请用简洁自然的方式将其转述给用户。
    以下是天气 JSON 数据：
    请将其转换为中文天气描述，例如：
    "北京现在天气：多云，气温 28℃，体感有点闷热（约 32℃），湿度 75%，微风（东南风 2 米/秒），
    能见度很好，大约 10 公里。建议穿短袖短裤。适合做户外运动。"
    """
)
output_parser = StrOutputParser()
output_chain = output_prompt | llm | output_parser

# ========== 4. 完整链：查询天气 → 适配数据结构 → 自然语言输出 ==========
full_chain = get_weather_chain | (lambda x: {"weather_json": x}) | output_chain

result = full_chain.invoke("请问北京今天的天气如何？")
logger.info(result)
