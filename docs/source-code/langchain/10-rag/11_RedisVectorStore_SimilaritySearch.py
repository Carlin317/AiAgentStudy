"""
[案例 10-11]在 Redis 向量库中做相似性检索(similarity_search_with_score)

知识点速览:
- 检索阶段:查询文本先向量化,再到向量库中找最接近的记录
- similarity_search_with_score(query, k) 返回 (Document, score) 列表
- 很多实现里 score 更接近"距离",越小越相似;此处 1-score 仅为直观展示
- 运行前需确保 Redis 中已有数据(先执行 RedisVectorStore.py)
"""

from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# ========== 1. 嵌入模型(与写入时一致) ==========
embeddings_model = DashScopeEmbeddings(
    model="text-embedding-v3", dashscope_api_key=os.getenv("aliQwen-api")
)

# ========== 2. 连接已有索引 ==========
vector_store = RedisVectorStore(
    embeddings_model,
    config=RedisConfig(index_name="newsgroups", redis_url="redis://localhost:26379"),
)

# ========== 3. 相似度检索 ==========
query = "我喜欢用什么手机"
results = vector_store.similarity_search_with_score(query, k=3)

print("=== 查询结果 ===")
for i, (doc, score) in enumerate(results, 1):
    # 近似换算成"相似度"仅为展示直观,工程里以具体返回定义为准
    similarity = 1 - score
    print(f"结果 {i}:")
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")
    print(f"相似度: {similarity:.4f}")

"""
[输出示例]
结果 1: 我喜欢用苹果手机  相似度: 0.8594
结果 2: 我喜欢吃苹果      相似度: 0.6610
"""
