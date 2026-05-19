"""
[案例 09-6]将 Document 列表向量化并写入 Redis(langchain_community)

知识点速览:
- Redis.from_documents() 自动对 page_content 向量化并连同 metadata 写入 Redis
- as_retriever() 得到检索器,invoke(查询) 时先向量化查询再做相似度检索
- redis_url 和 index_name 需与本地环境一致;复用已有索引时两端必须同名
"""

# pip install langchain-community dashscope redis redisvl
import os
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# ========== 1. 初始化嵌入模型 ==========
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3", dashscope_api_key=os.getenv("aliQwen-api")
)

# ========== 2. 构造 Document 列表 ==========
texts = [
    "通义千问是阿里巴巴研发的大语言模型.",
    "Redis 是一个高性能的键值存储系统,支持向量检索.",
    "LangChain 可以轻松集成各种大模型和向量数据库.",
]
documents = [
    Document(page_content=text, metadata={"source": "manual"}) for text in texts
]

# ========== 3. 向量化并写入 Redis ==========
vector_store = Redis.from_documents(
    documents=documents,
    embedding=embeddings,
    redis_url="redis://localhost:26379",
    index_name="my_index11",
)

# ========== 4. 相似度检索 ==========
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
results = retriever.invoke("LangChain 和 Redis 怎么结合?")
for res in results:
    print(res.page_content)
