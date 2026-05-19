"""
[案例 02-3]使用 init_chat_model 统一入口调用大模型(1.0 推荐写法)

对应教程章节:第 11 章 - Model I/O 与模型接入 → 3,接入大模型

知识点速览:
- init_chat_model 统一入口,同一套骨架可切换不同模型和 provider
- invoke() 既可接单条字符串,也可接多角色消息列表
- 部分模型名(如 qwen-plus)无法自动推断 provider,仍需显式指定
"""

# ========== 1. 导入与环境 ==========
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

# ========== 2. 实例化模型 ==========
# 本例选择 DeepSeek 可自动推断 provider;qwen-plus 等模型名则需显式指定 model_provider
model = init_chat_model(
    model="deepseek-v4-flash",
    api_key=os.getenv("deepseek-api"),
    base_url="https://api.deepseek.com",
)

# ========== 3. 调用并取正文 ==========
# 写法一:传入字符串(框架自动包装为 user 消息,无法单独设 system)
print(model.invoke("你是谁?").content)

# 写法二:多角色消息列表(可设 system)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁?"},
]
response = model.invoke(messages)
print(response.content)
