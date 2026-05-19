"""
[案例 06-2]多步串行链:前一步输出作为后一步输入

对应教程章节:第 15 章 - LCEL 与链式调用 → 4.3 多步串行链(Multi-Step Chain)

知识点速览:
- 多步串行链中,前一步的输出直接流向后一步
- 前后子链输入输出结构不匹配时,需要插入 lambda 做数据适配
- 本例:chain1 输出 str → lambda 转为 {"input": str} → chain2 接收并翻译
"""

import os

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 1. 子链 1:中文介绍某主题 ==========
prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个知识渊博的计算机专家,请用中文简短回答"),
        ("human", "请简短介绍什么是{topic}"),
    ]
)
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

result1 = chain1.invoke({"topic": "langchain"})
logger.info(result1)

# ========== 2. 子链 2:翻译成英文 ==========
prompt2 = ChatPromptTemplate.from_messages(
    [("system", "你是一个翻译助手,将用户输入内容翻译成英文"), ("human", "{input}")]
)
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2

# ========== 3. 串行组合 ==========
# lambda 将 chain1 的 str 输出适配为 chain2 需要的 {"input": ...} 结构
full_chain = chain1 | (lambda content: {"input": content}) | chain2

result = full_chain.invoke({"topic": "langchain"})
logger.info(result)
