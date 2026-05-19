"""
[案例 06-5]分支链:根据输入条件选择不同子链执行

对应教程章节:第 15 章 - LCEL 与链式调用 → 4.2 RunnableBranch(分支链)

知识点速览:
- RunnableBranch 按顺序判断 (条件, Runnable) 对,命中的第一条分支被执行
- 最后一个未成对的 Runnable 为默认分支
- 每个分支内部仍可是 prompt | model | parser 顺序链
"""

import os

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch
from loguru import logger

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

# ========== 1. 定义各语言分支的提示词模板 ==========
english_prompt = ChatPromptTemplate.from_messages(
    [("system", "你是一个英语翻译专家"), ("human", "{query}")]
)

japanese_prompt = ChatPromptTemplate.from_messages(
    [("system", "你是一个日语翻译专家"), ("human", "{query}")]
)

korean_prompt = ChatPromptTemplate.from_messages(
    [("system", "你是一个韩语翻译专家"), ("human", "{query}")]
)


# ========== 2. 语言检测函数 ==========
def determine_language(inputs):
    """根据 query 中的关键词判断目标语言."""
    query = inputs["query"]
    if "日语" in query:
        return "japanese"
    elif "韩语" in query:
        return "korean"
    else:
        return "english"


# ========== 3. 构建分支链 ==========
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

parser = StrOutputParser()

chain = RunnableBranch(
    (lambda x: determine_language(x) == "japanese", japanese_prompt | model | parser),
    (lambda x: determine_language(x) == "korean", korean_prompt | model | parser),
    (english_prompt | model | parser),  # 默认分支
)

# ========== 4. 测试不同语言输入 ==========
test_queries = [
    {"query": '请你用韩语翻译这句话:"见到你很高兴"'},
    {"query": '请你用日语翻译这句话:"见到你很高兴"'},
    {"query": '请你用英语翻译这句话:"见到你很高兴"'},
]

for query_input in test_queries:
    lang = determine_language(query_input)
    logger.info(f"检测到语言类型: {lang}")

    if lang == "japanese":
        selected_prompt = japanese_prompt
    elif lang == "korean":
        selected_prompt = korean_prompt
    else:
        selected_prompt = english_prompt

    formatted_messages = selected_prompt.format_messages(**query_input)
    logger.info("格式化后的提示词:")
    for msg in formatted_messages:
        logger.info(f"[{msg.type}]: {msg.content}")

    result = chain.invoke(query_input)
    logger.info(f"输出结果: {result}\n")
