"""
[案例 06-3]并行链:同时运行多条子链,汇总结果

对应教程章节:第 15 章 - LCEL 与链式调用 → 4.4 RunnableParallel(并行链)

知识点速览:
- RunnableParallel 将同一输入同时喂给多条子链,结果按键名汇总为 dict 返回
- 除了显式写 RunnableParallel({...}),也可直接用字典字面量表达并行结构
- 并行完成后,可继续将 dict 交给后续链做总结或比较
"""

import os

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from loguru import logger

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 1. 子链 1:中文简短介绍 ==========
prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个知识渊博的计算机专家,请用中文简短回答"),
        ("human", "请简短介绍什么是{topic}"),
    ]
)
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

# ========== 2. 子链 2:英文简短介绍 ==========
prompt2 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个知识渊博的计算机专家,请用英文简短回答"),
        ("human", "请简短介绍什么是{topic}"),
    ]
)
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2

# ========== 3. 并行执行 ==========
parallel_chain = RunnableParallel({"chinese": chain1, "english": chain2})

result = parallel_chain.invoke({"topic": "langchain"})
logger.info(result)

# 打印 ASCII 图结构,便于理解数据流
parallel_chain.get_graph().print_ascii()
