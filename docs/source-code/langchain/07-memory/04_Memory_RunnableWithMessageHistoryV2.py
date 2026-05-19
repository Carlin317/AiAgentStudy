"""
[案例 07-4]自动管理对话历史(多会话):按 session_id 维护多份 InMemoryChatMessageHistory

对应教程章节:第 16 章 - 记忆与对话历史 → 6,案例代码 → 6.1 内存版

知识点速览:
- 与单会话版的区别:get_session_history() 从 store 中按 session_id 取不同 history
- 可支持多用户/多会话,每个 session 拥有独立的历史
- 生产环境可将 store 换成 Redis 等,get_session_history 返回 RedisChatMessageHistory 即可
"""

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import os

llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 1. 按 session_id 存储多份历史 ==========
store = {}


def get_session_history(session_id: str):
    """根据 session_id 获取对应的历史消息对象,不存在则新建."""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# ========== 2. 构建带历史的链 ==========
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个友好的中文助理,会根据上下文回答问题."),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ]
)
memory_chain = prompt | llm | StrOutputParser()

with_history = RunnableWithMessageHistory(
    memory_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# ========== 3. 多会话交叉测试 ==========
cfg_user_001 = {"configurable": {"session_id": "user-001"}}
cfg_user_002 = {"configurable": {"session_id": "user-002"}}

print("用户A(user-001):我叫张三.")
print("AI:", with_history.invoke({"question": "我叫张三."}, cfg_user_001))

print("\n用户B(user-002):我叫李四.")
print("AI:", with_history.invoke({"question": "我叫李四."}, cfg_user_002))

print("\n用户A(user-001):我叫什么?")
print("AI:", with_history.invoke({"question": "我叫什么?"}, cfg_user_001))

print("\n用户B(user-002):我叫什么?")
print("AI:", with_history.invoke({"question": "我叫什么?"}, cfg_user_002))

# ========== 4. 查看 store 中的历史数据 ==========
print("\n--- 当前 store 中的历史数据 ---")
for sid, hist in store.items():
    print(f"[session_id={sid}] 共 {len(hist.messages)} 条消息:")
    for i, msg in enumerate(hist.messages):
        content = str(msg.content)
        content_preview = (content[:50] + "...") if len(content) > 50 else content
        print(f"  {i+1}. [{msg.type}] {content_preview}")
print("--- end ---\n")
