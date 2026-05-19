"""
[案例 09-1]DashScope 原生调用:单句文本向量化(Hello 级)

知识点速览:
- Embedding 把文本变成一串数字(向量),后续语义检索,RAG 都依赖此结果
- dashscope.TextEmbedding.call() 传入模型名和文本即可返回向量
- 向量从 output.embeddings[0].embedding 获取,长度由模型决定

模型文档:https://bailian.console.aliyun.com/cn-beijing/?productCode=p_efm&tab=doc#/doc/?type=model&url=2842587
"""

import os
import dashscope
from http import HTTPStatus
from dotenv import load_dotenv

load_dotenv()
dashscope.api_key = os.getenv("aliQwen-api")

input_text = "衣服的质量杠杠的"

# ========== 1. 调用百炼文本嵌入接口 ==========
resp = dashscope.TextEmbedding.call(
    model="text-embedding-v4",
    input=input_text,
)

if resp.status_code == HTTPStatus.OK:
    print(resp)

"""
[输出示例]
{"status_code": 200, "request_id": "0a76a5db-f4af-4e5a-b0c4-1689d81ba154", "code": "", "message": "", "output": {"embeddings": [{"embedding": [0.02258586511015892, -0.08700370043516159, -0.013521800749003887, -0.05904024466872215, 0.027100207284092903, -0.03104848973453045, 0.01432843878865242, -0.0008265386568382382,……], "text_index": 0}]}, "usage": {"total_tokens": 6}}
"""
