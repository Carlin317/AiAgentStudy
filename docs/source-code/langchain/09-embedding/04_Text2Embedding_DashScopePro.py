"""
[案例 09-4]DashScope 多模态 Embedding:文本/图像向量化(进阶)

知识点速览:
- 多模态嵌入模型可同时处理文本和图像,input 列表项可为 {"text": "..."} 或 {"image": "url"}
- 返回结构与单模态类似,output.embeddings 为列表,每项含 embedding 向量
- 本例只演示文本输入,图像输入通常需要 URL 或 base64

模型文档:https://bailian.console.aliyun.com/?productCode=p_efm&tab=model#/model-market/all?capabilities=ME
"""

import dashscope
import json
import os
from http import HTTPStatus
from dotenv import load_dotenv

load_dotenv()
# MultiModalEmbedding.call 内部用 get_default_api_key(),必须提前设置
dashscope.api_key = os.getenv("aliQwen-api")

# ========== 1. 调用多模态 Embedding 接口 ==========
resp = dashscope.MultiModalEmbedding.call(
    model="tongyi-embedding-vision-plus",
    input=[{"text": "尚硅谷AI"}],
)

result = ""

if resp.status_code == HTTPStatus.OK:
    result = {
        "status_code": resp.status_code,
        "request_id": getattr(resp, "request_id", ""),
        "code": getattr(resp, "code", ""),
        "message": getattr(resp, "message", ""),
        "output": resp.output,
        "usage": resp.usage,
    }
    print(json.dumps(result, ensure_ascii=False, indent=4))

print("=================================")
print()

# ========== 2. 提取向量 ==========
embedding_values = result["output"]["embeddings"][0]["embedding"]
print(json.dumps(embedding_values, ensure_ascii=False))
