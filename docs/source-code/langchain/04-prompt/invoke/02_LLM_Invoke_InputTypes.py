“””
【案例 04-2】invoke / ainvoke 的多种输入类型（字符串、Message 列表、元组列表、字典列表）

对应教程章节：第 13 章 → 2、调用大模型的入参类型

知识点速览：
- invoke 支持多种输入格式：Message 对象列表、(role, content) 元组列表、字典列表
- 框架内部统一转为消息表示，输出均为 AIMessage
- Message 类写法角色最清晰，元组/字典写法更简洁
“””

import asyncio
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def demo_message_objects():
    """推荐：显式 Message 对象，角色与字段最清晰。"""
    messages = [
        SystemMessage(content="你是一个专业的数学助手，回答要简短。"),
        HumanMessage(content="你好，你是谁？"),
    ]
    resp = model.invoke(messages)
    print(type(resp), resp.content[:80] if resp.content else "")


def demo_tuple_list():
    """元组列表：与 ChatPromptTemplate.from_messages 的写法一致。"""
    messages = [
        ("system", "你是一个专业的数学助手，回答要简短。"),
        ("human", "你好，你是谁？"),
    ]
    resp = model.invoke(messages)
    print(type(resp), resp.content[:80] if resp.content else "")


def demo_dict_list():
    """字典列表：与 OpenAI Chat Completions 等 API 的请求体形状接近。"""
    messages = [
        {"role": "system", "content": "你是一个专业的数学助手，回答要简短。"},
        {"role": "user", "content": "你好，你是谁？"},
    ]
    resp = model.invoke(messages)
    print(type(resp), resp.content[:80] if resp.content else "")


async def demo_ainvoke_tuple():
    """异步调用同样支持元组简写。"""
    resp = await model.ainvoke([("user", "用一句话说明什么是素数")])
    print(type(resp), resp.content[:80] if resp.content else "")


if __name__ == "__main__":
    print("--- Message 对象列表 ---")
    demo_message_objects()
    print("--- 元组列表 ---")
    demo_tuple_list()
    print("--- 字典列表 ---")
    demo_dict_list()
    print("--- ainvoke + 元组 ---")
    asyncio.run(demo_ainvoke_tuple())

"""
【输出示例】
--- Message 对象列表 ---
<class 'langchain_core.messages.ai.AIMessage'> 我是Qwen，阿里巴巴研发的超大规模语言模型。
--- 元组列表 ---
<class 'langchain_core.messages.ai.AIMessage'> 我是Qwen，阿里巴巴研发的超大规模语言模型。
--- 字典列表 ---
<class 'langchain_core.messages.ai.AIMessage'> 我是Qwen，阿里巴巴研发的超大规模语言模型。
--- ainvoke + 元组 ---
<class 'langchain_core.messages.ai.AIMessage'> 素数（或质数）是指大于1的自然数中，除了1和它本身之外不再有其他正因数的数。
"""
