"""
[案例 05-6]用 TypedDict + Annotated 做结构化输出

对应教程章节:第 14 章 - 输出解析器 → 3,结构化输出(TypedDict / Pydantic / Annotated)

知识点速览:
- with_structured_output(类型) 让模型按指定结构生成并自动解析,无需手写 Parser
- TypedDict + Annotated 可为字段添加描述元数据,帮助模型理解各字段含义
- 调用 .invoke() 后直接得到符合结构的 dict
"""

import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(encoding="utf-8")

# ========== 1. 初始化大模型 ==========
llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


# ========== 2. 定义输出结构 ==========
class Animal(TypedDict):
    animal: Annotated[str, "动物"]
    emoji: Annotated[str, "表情"]


class AnimalList(TypedDict):
    animals: Annotated[list[Animal], "动物与表情列表"]


# ========== 3. 绑定结构化输出并调用 ==========
messages = [{"role": "user", "content": "任意生成三种动物,以及它们的 emoji 表情"}]

llm_with_structured_output = llm.with_structured_output(AnimalList)
resp = llm_with_structured_output.invoke(messages)
print(resp)

"""
[输出示例]
{'animals': [{'animal': '狗', 'emoji': '🐶'}, {'animal': '猫', 'emoji': '🐱'}, {'animal': '鸟', 'emoji': '🐦'}]}
"""
