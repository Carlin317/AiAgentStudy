"""
[案例 07-3]自动管理对话历史(单会话):RunnableWithMessageHistory + InMemoryChatMessageHistory

对应教程章节:第 16 章 - 记忆与对话历史 → 6,案例代码 → 6.1 内存版

知识点速览:
- RunnableWithMessageHistory 在 invoke 时自动完成:取历史 → 拼入 Prompt → 执行链 → 写回历史
- InMemoryChatMessageHistory 数据存在进程内存,重启即丢失
- 本例固定返回同一个 history,仅演示单会话连续对话
- 多 session 写法见 Memory_RunnableWithMessageHistoryV2.py
"""

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
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

# ========== 1. 构建带历史占位符的链 ==========
prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
parser = StrOutputParser()
chain = prompt | llm | parser

# ========== 2. 包装为带历史版本 ==========
history = InMemoryChatMessageHistory()

runnable = RunnableWithMessageHistory(
    chain,
    get_session_history=lambda session_id: history,
    input_messages_key="input",
    history_messages_key="history",
)
history.clear()
config = RunnableConfig(configurable={"session_id": "user-001"})

# ========== 3. 多轮对话 ==========
logger.info(runnable.invoke({"input": "我叫张三,我爱好学习."}, config))
logger.info(runnable.invoke({"input": "我叫什么?我的爱好是什么?"}, config))
