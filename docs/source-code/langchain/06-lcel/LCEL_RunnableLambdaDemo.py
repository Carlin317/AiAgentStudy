"""
【案例 06-4】函数链：用 RunnableLambda 将普通 Python 函数接入 LCEL 链

对应教程章节：第 15 章 - LCEL 与链式调用 → 4.5 RunnableLambda（函数链）

知识点速览：
- RunnableLambda 将普通 Python 函数包装为 Runnable 节点，可插入 LCEL 链
- 适合做轻量逻辑：打印中间结果、字段映射、输入输出结构适配
- 直接把函数放在 | 之间时 LangChain 会自动包装，等价于显式 RunnableLambda(func)
"""

import os

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from loguru import logger

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    temperature=0.0,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def debug_print(x):
    """打印中间结果，并将文本包装为 chain2 所需的 {"input": 文本} 结构。"""
    logger.info(f"中间结果:{x}")
    return {"input": x}


# ========== 1. 子链 1：中文介绍某主题 ==========
prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
        ("human", "请简短介绍什么是{topic}"),
    ]
)
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

# ========== 2. 子链 2：翻译成英文 ==========
prompt2 = ChatPromptTemplate.from_messages(
    [("system", "你是一个翻译助手，将用户输入内容翻译成英文"), ("human", "{input}")]
)
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2

# ========== 3. 方式一：函数直接放在 | 之间（自动包装） ==========
full_chain = chain1 | debug_print | chain2
result1 = full_chain.invoke({"topic": "langchain"})
logger.info(f"最终结果（自动包装）:{result1}")

# ========== 4. 方式二：显式使用 RunnableLambda ==========
debug_node = RunnableLambda(debug_print)
full_chain = chain1 | debug_node | chain2
result2 = full_chain.invoke({"topic": "langchain"})
logger.info(f"最终结果（显式包装）:{result2}")
