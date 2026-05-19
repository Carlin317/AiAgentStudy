"""
[案例 06-1]顺序链:Prompt → Model → Parser 一条线执行

对应教程章节:第 15 章 - LCEL 与链式调用 → 4.1 RunnableSequence(顺序链)

知识点速览:
- LCEL 用管道符 `|` 将多个 Runnable 串联,组合后的对象类型为 RunnableSequence
- prompt,model,parser 均实现 Runnable 接口,可单独 invoke() 也可组合后整体 invoke()
- 组合后一次 invoke 即完成"渲染 → 模型调用 → 解析"全流程
"""

import os

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

# ========== 1. 分步执行:逐个 invoke ==========
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{role},请简短回答我提出的问题"),
        ("human", "请回答:{question}"),
    ]
)

prompt = chat_prompt.invoke(
    {"role": "AI助手", "question": "什么是LangChain,简洁回答100字以内"}
)
logger.info(prompt)

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

result = model.invoke(prompt)
logger.info(f"模型原始输出:\n{result}")

parser = StrOutputParser()

response = parser.invoke(result)
logger.info(f"解析后的结果:\n{response}")
logger.info(f"结果类型: {type(response)}")  # <class 'str'>

print()
print("*" * 60)
print()

# ========== 2. 链式执行:用 | 组合后一次 invoke ==========
chain = chat_prompt | model | parser

result_chain = chain.invoke(
    {"role": "AI助手", "question": "什么是LangChain,简洁回答100字以内"}
)
logger.info(f"Chain执行结果:\n{result_chain}")
logger.info(f"Chain执行结果类型: {type(result_chain)}")  # <class 'str'>

print(type(chain))  # <class 'langchain_core.runnables.base.RunnableSequence'>
