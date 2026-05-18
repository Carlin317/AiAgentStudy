"""
【案例 09-3】LangChain DashScope 封装：单条与批量文本向量化

知识点速览：
- embed_query(text)：查询阶段，把用户问题转成向量
- embed_documents(texts)：索引阶段，把文档片段批量转成向量
- 建索引和查询时应保持模型一致，否则向量空间不匹配

模型文档：https://bailian.console.aliyun.com/cn-beijing/?tab=api#/api/?type=model&url=2587654
"""

# pip install langchain-community dashscope
import os
from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

load_dotenv()

# DashScopeEmbeddings 默认读 DASHSCOPE_API_KEY，此处显式传入项目统一的 key
embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=os.getenv("aliQwen-api"),
)

text = "This is a test document."

# ========== 1. 单条文本向量化 ==========
query_result = embeddings.embed_query(text)
print("文本向量长度：", len(query_result), sep="")

# ========== 2. 批量文本向量化 ==========
doc_results = embeddings.embed_documents(
    [
        "Hi there!",
        "Oh, hello!",
        "What's your name?",
        "My friends call me World",
        "Hello World!",
    ]
)
print(doc_results)
print(
    "文本向量数量：", len(doc_results), "，文本向量长度：", len(doc_results[0]), sep=""
)
