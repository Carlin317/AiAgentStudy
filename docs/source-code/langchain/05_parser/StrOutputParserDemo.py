"""
【案例 05-3】StrOutputParser 字符串解析器

对应教程章节：第 14 章 - 输出解析器 → 2、常用输出解析器用法

知识点速览：
- StrOutputParser 从 AIMessage 中提取 content 字段，返回纯字符串（str）
- 适合只需文本内容、不需要结构化解析的场景
- 典型流程：Prompt → model.invoke() → parser.invoke() → str
- 相比直接取 result.content，解析器可链式组合（prompt | model | parser）且接口统一
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from loguru import logger

load_dotenv(encoding="utf-8")

# ========== 1. 构造对话模板 ==========
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{role}，请简短回答我提出的问题"),
        ("human", "请回答:{question}"),
    ]
)

prompt = chat_prompt.invoke(
    {"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"}
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

# StrOutputParser：从 AIMessage 取 content 转为 str
# 好处：可链式组合、流式统一处理 chunk、与其他 Parser 接口一致便于替换
parser = StrOutputParser()

response = parser.invoke(result)
logger.info(f"解析后的结果:\n{response}")
logger.info(f"结果类型: {type(response)}")  # <class 'str'>
