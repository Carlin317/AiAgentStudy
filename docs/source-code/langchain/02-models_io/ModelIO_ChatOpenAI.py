“””
【案例 02-2】使用 LangChain ChatOpenAI 调用大模型（OpenAI 兼容接口）

对应教程章节：第 11 章 - Model I/O 与模型接入 → 3、接入大模型

知识点速览：
- ChatOpenAI + base_url 接入国内兼容接口，可与 Prompt / Chain / Agent 等组件配合
- 返回 AIMessage，用 .content 取正文；元数据见 .response_metadata
- 与 ModelIO_OpenAI.py 的区别：LangChain 封装 vs 原生 SDK
“””

# ========== 1. 导入与环境 ==========
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv(encoding=”utf-8”)

# ========== 2. 初始化聊天模型（OpenAI 兼容接口） ==========
chat_llm = ChatOpenAI(
    model=”qwen-plus”,
    api_key=os.getenv(“aliQwen-api”),
    base_url=”https://dashscope.aliyuncs.com/compatible-mode/v1”,
)

# ========== 3. 调用模型并打印回复 ==========
messages = [
    {“role”: “system”, “content”: “You are a helpful assistant.”},
    {“role”: “user”, “content”: “你是谁？”},
]

response = chat_llm.invoke(messages)
print(response.content)
