"""
【案例 09-5】通过向量计算语义相似度：余弦相似度

知识点速览：
- 文本转成向量后，可用余弦相似度衡量语义接近程度：值在 [-1, 1]，越接近 1 越相似
- 公式：cos(theta) = (A . B) / (|A| * |B|)
- 常用于检索排序、文本去重、聚类、推荐等任务
"""

import dashscope
import os
from http import HTTPStatus
import numpy as np
from dotenv import load_dotenv

load_dotenv()

texts = ["我喜欢吃苹果", "苹果是我最喜欢吃的水果", "我喜欢用苹果手机"]

# ========== 1. 批量获取文本向量 ==========
embeddings = []
for text in texts:
    input_data = [{"text": text}]
    resp = dashscope.MultiModalEmbedding.call(
        model="multimodal-embedding-v1",
        api_key=os.getenv("aliQwen-api"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        input=input_data,
    )
    if resp.status_code == HTTPStatus.OK:
        embedding = resp.output["embeddings"][0]["embedding"]
        embeddings.append(embedding)


# ========== 2. 余弦相似度计算 ==========
def cosine_similarity(vec1, vec2):
    """点积 / (模长之积)"""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


# ========== 3. 两两比较 ==========
print("文本相似度比较结果:")
print("=" * 60)

for i in range(len(texts)):
    for j in range(i + 1, len(texts)):
        similarity = cosine_similarity(embeddings[i], embeddings[j])
        print(f"文本{i+1} vs 文本{j+1}:")
        print(f"  文本{i+1}: {texts[i]}")
        print(f"  文本{j+1}: {texts[j]}")
        print(f"  余弦相似度: {similarity:.4f}")
        print("-" * 40)

"""
【输出示例】
文本1 vs 文本2:  余弦相似度: 0.9064  （语义接近：都是"吃苹果"）
文本1 vs 文本3:  余弦相似度: 0.7656  （字面重叠但语义不同：水果 vs 手机）
文本2 vs 文本3:  余弦相似度: 0.7421
"""
