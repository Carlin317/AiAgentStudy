"""
[案例 05-4]JsonOutputParser 基础用法:在提示词中直接要求返回 JSON

对应教程章节:第 14 章 - 输出解析器 → 2,常用输出解析器用法

知识点速览:
- JsonOutputParser 将模型文本输出解析为 dict / list
- 本案例在 system 提示词中手写格式要求,适合结构简单的场景
- 进阶做法见 JsonOutputParser_GetFormatInstructions.py:用 get_format_instructions() 自动生成格式说明
"""

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from loguru import logger

load_dotenv(encoding="utf-8")

# ========== 1. 构造对话模板 ==========
# 在 system 消息中直接写明:返回 json,包含 q(问题),a(答案)字段
chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个{role},请简短回答我提出的问题,结果返回json格式,q字段表示问题,a字段表示答案.",
        ),
        ("human", "请回答:{question}"),
    ]
)

prompt = chat_prompt.invoke(
    {"role": "AI助手", "question": "什么是LangChain,简洁回答100字以内"}
)
logger.info(prompt)

# ========== 2. 初始化大模型 ==========
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 3. 调用模型并解析 ==========
result = model.invoke(prompt)
logger.info(f"模型原始输出:\n{result}")

# 不绑 Pydantic 时,解析结果为 dict/list
parser = JsonOutputParser()
response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")
logger.info(f"结果类型: {type(response)}")  # <class 'dict'>
