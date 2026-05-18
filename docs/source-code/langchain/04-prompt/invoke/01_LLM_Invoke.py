“””
【案例 04-1】模型调用：同步 invoke（单次调用，一次性返回）

对应教程章节：第 13 章 - 提示词与消息模板 → 4、调用大模型的调用方式

知识点速览：
- invoke 是最常用的同步调用方式，等待模型完整生成后一次性返回 AIMessage
- SystemMessage + HumanMessage 让模型区分”系统规则”和”用户问题”
- 返回值通过 .content 取正文，.content_blocks 取结构化内容块
“””

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# ========== 1. 实例化聊天模型 ==========
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 2. 构建多角色消息列表 ==========
messages = [
    SystemMessage(
        content="你是一个法律助手，只回答法律问题，超出范围的统一回答，非法律问题无可奉告"
    ),
    HumanMessage(content="简单介绍下广告法，一句话告知50字以内"),
]

# ========== 3. 同步调用模型（invoke） ==========
response = model.invoke(messages)
print(f"响应类型：{type(response)}")  # AIMessage
print(response.content)
print(response.content_blocks)

"""
【输出示例】
响应类型：<class 'langchain_core.messages.ai.AIMessage'>
《广告法》是规范广告活动、保护消费者权益、维护市场秩序的法律，禁止虚假宣传、误导欺诈等行为。
[{'type': 'text', 'text': '《广告法》是规范广告活动、保护消费者权益、维护市场秩序的法律，禁止虚假宣传、误导欺诈等行为。'}]
"""
