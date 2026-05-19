"""
[案例 04-3]模型调用:同步 stream(流式输出)

对应教程章节:第 13 章 - 提示词与消息模板 → 4,调用大模型的调用方式

知识点速览:
- stream 返回生成器,逐块 yield AIMessageChunk,实现"打字机"效果
- 适合聊天界面和长文本生成场景
- 与 invoke 的区别:invoke 一次性返回 AIMessage,stream 逐块返回
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# ========== 1. 实例化模型 ==========
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 2. 构建多角色消息 ==========
messages = [
    SystemMessage(content="你叫小问,是一个乐于助人的AI人工助手"),
    HumanMessage(content="你是谁"),
]

# ========== 3. 流式调用 ==========
response = model.stream(messages)
print(f"响应类型:{type(response)}")  # generator

for chunk in response:
    print(chunk.content, end="", flush=True)
print("\n")

"""
[输出示例]
响应类型:<class 'generator'>
你好呀!我是小问,一个乐于助人的AI人工助手～😊
我擅长解答问题,帮你理清思路,写文案,做学习规划,整理资料,甚至陪你聊聊天,出出主意.不管是学习上的难题,工作中的困惑,还是生活里的小烦恼,我都很乐意倾听和帮忙!
"""
