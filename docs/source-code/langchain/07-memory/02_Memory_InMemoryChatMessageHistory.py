"""
【案例 07-2】手动管理对话历史：直接使用 InMemoryChatMessageHistory API

对应教程章节：第 16 章 - 记忆与对话历史 → 5、实现类介绍 / 6.1 内存版

知识点速览：
- InMemoryChatMessageHistory 提供 add_message()、add_user_message()、messages 等 API
- 手动维护时需自行决定何时写入用户消息、何时写回 AI 回复
- 漏掉 add_message(ai_message) 会导致下一轮模型看不到自己的上一轮回答
- 多数场景更推荐用 RunnableWithMessageHistory 自动完成读写
"""

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from loguru import logger
import os

llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 1. 创建内存版历史实例 ==========
history = InMemoryChatMessageHistory()

# ========== 2. 第一轮对话 ==========
history.add_user_message("我叫张三，我的爱好是学习")
ai_message = llm.invoke(history.messages)
logger.info(f"第一次回答\n{ai_message.content}")
# 必须手动把 AI 回复写回 history，否则下一轮不会有上下文
history.add_message(ai_message)

# ========== 3. 第二轮对话 ==========
history.add_user_message("我叫什么？我的爱好是什么？")
ai_message2 = llm.invoke(history.messages)
logger.info(f"第二次回答\n{ai_message2.content}")
history.add_message(ai_message2)

# ========== 4. 查看全部消息 ==========
for index, message in enumerate(history.messages, start=1):
    logger.info(f"第{index}条[{message.type}] {message.content}")
