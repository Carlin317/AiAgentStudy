"""
[案例 07-1]无记忆演示:两轮请求相互独立,模型无法利用上一轮内容

对应教程章节:第 16 章 - 记忆与对话历史 → 3,"我不知道"演示:无记忆时的行为

知识点速览:
- 仅用 Prompt + Model + Parser 且不保存历史时,每次 invoke 相互独立
- 本案例先告诉模型"我叫张三",再问"你知道我是谁吗",第二问模型会回答"不知道"
- 网页版聊天能记住多轮,是因为应用层实现了历史读写,而非模型本身记住了
"""

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
import os

# ========== 1. 构建无记忆的简单链 ==========
llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    temperature=0.0,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
prompt = PromptTemplate.from_template("请回答我的问题:{question}")
parser = StrOutputParser()
chain = prompt | llm | parser

# ========== 2. 两轮独立调用 ==========
# 第一轮:告诉模型"我叫张三"
print(chain.invoke({"question": "我叫张三,你叫什么?"}))

# 第二轮:模型无法看到上一轮,会回答"我不知道"
print(chain.invoke({"question": "你知道我是谁吗?"}))
