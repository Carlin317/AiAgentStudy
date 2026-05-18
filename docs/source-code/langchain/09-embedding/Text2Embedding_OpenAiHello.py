"""
【案例 09-2】OpenAI 兼容接口调用阿里百炼 Embedding（Hello 级）

知识点速览：
- 同一类 Embedding 能力可通过 OpenAI 兼容协议调用，切换厂商时只需调整 base_url/api_key/model
- client.embeddings.create() 的 input 可以是单字符串或字符串列表
- 返回结果中 data[i].embedding 即为向量
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

input_text = "衣服的质量杠杠的"

# ========== 1. 通过 OpenAI 兼容接口连接百炼 ==========
client = OpenAI(
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 2. 调用 Embedding ==========
completion = client.embeddings.create(model="text-embedding-v4", input=input_text)

print(completion.model_dump_json())

"""
【输出示例】
注：embedding 共 1024 维度，即 len(completion.data[0].embedding) == 1024
{"data":[{"embedding":[0.02258586511015892,-0.08700370043516159,...],"index":0,"object":"embedding"}],"model":"text-embedding-v4","object":"list","usage":{"prompt_tokens":6,"total_tokens":6},"id":"37989997-27b1-9416-98af-091ae0b5c118"}
"""
