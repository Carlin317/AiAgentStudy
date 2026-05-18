"""
【案例 10-10】使用 langchain_redis 将文本写入 Redis 向量库（add_texts）

知识点速览：
- 纯文本流入库路线：先创建 RedisVectorStore，再通过 add_texts() 写入
- add_texts() 内部调用 embed_documents() 做批量向量化，再连同 metadata 写入 Redis
- 与 from_documents() 不冲突：前者适合纯文本列表，后者适合 Document 列表
- 返回的 ids 可用于更新、删除或追踪
"""

from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# ========== 1. 初始化嵌入模型 ==========
embeddings_model = DashScopeEmbeddings(
    model="text-embedding-v3", dashscope_api_key=os.getenv("aliQwen-api")
)

# ========== 2. 待写入的文本 ==========
texts = [
    "我喜欢吃苹果",
    "苹果是我最喜欢吃的水果",
    "我喜欢用苹果手机",
]

# 批量转向量：仅用于观察向量维度，add_texts 内部会再次完成向量化
embeddings = embeddings_model.embed_documents(texts)
for i, vec in enumerate(embeddings, 1):
    print(f"文本 {i}: {texts[i-1]}")
    print(f"向量长度: {len(vec)}")
    print(f"前 10 个向量值: {vec[:10]}\n")

# ========== 3. 元数据 ==========
metadata = [{"segment_id": str(i)} for i in range(1, len(texts) + 1)]

# ========== 4. 连接 Redis 并写入 ==========
config = RedisConfig(
    index_name="newsgroups",
    redis_url="redis://localhost:26379",
)

vector_store = RedisVectorStore(embeddings_model, config=config)

ids = vector_store.add_texts(texts, metadata)

print(ids[0:5])

"""
【输出示例】
文本 1: 我喜欢吃苹果
向量长度: 1024
前 10 个向量值: [-0.0406..., 0.0366..., ...]
……
['newsgroups:01KKDZ5MRGBDPWJHDZZWH4W2Q6', ...]
"""
