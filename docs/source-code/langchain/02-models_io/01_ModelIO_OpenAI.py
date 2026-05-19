"""
[案例 02-1]使用 OpenAI 官方 SDK 直接调用大模型(不经过 LangChain)

对应教程章节:第 11 章 - Model I/O 与模型接入 → 3,接入大模型

知识点速览:
- 原生 OpenAI SDK 调用,与 ChatOpenAI / init_chat_model 做边界对比
- 返回值是 SDK 原生结构,取正文需 response.choices[0].message.content
- 适合不需要 Prompt / Chain / Agent 等 LangChain 组件的简单场景
"""

# ========== 1. 导入与环境 ==========
import os
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

# ========== 2. 初始化客户端 ==========
client = OpenAI(
    api_key=os.getenv("deepseek-api"),
    base_url="https://api.deepseek.com",
)

# ========== 3. 发起对话并打印回复 ==========
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello,你是谁?"},
    ],
    stream=False,
)

# 原生 SDK 的取值路径与 LangChain 的 AIMessage.content 不同
print(response.choices[0].message.content)
