"""
[案例 01-3]LangChain 1.0 写法:init_chat_model 统一入口调用大模型

对应教程章节:第 10 章 - LangChain 快速上手与 HelloWorld → 4,实战:基于阿里百炼的 HelloWorld

知识点速览:
- init_chat_model 是 1.0 统一入口,通过 model_provider 指定厂商,同一套写法可切换模型
- 国内平台(阿里百炼等)需显式写 model_provider="openai",否则无法推断 provider
- 同一脚本可创建多个模型实例,按需调用
"""

# ========== 1. 导入依赖 ==========
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(encoding="utf-8")

# ========== 2. 实例化模型并调用 ==========
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",  # 阿里百炼需通过 OpenAI 兼容接口调用
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

print(model.invoke("你是谁").content)

print("*" * 50)

# 不写 model_provider="openai" 会报 ValueError: Unable to infer model provider
# 因为 qwen-plus 等名称无法自动推断厂商;对比 0.x 的 ChatOpenAI 类名已隐含 provider

# 同一脚本可同时存在多个模型实例
model2 = init_chat_model(
    model="deepseek-v3",
    model_provider="openai",
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

print(model2.invoke("你是谁").content)

"""
[输出示例]
你好!我是通义千问(Qwen),阿里巴巴集团旗下的超大规模语言模型.我能够回答问题,创作文字,比如写故事,写公文,写邮件,写剧本,逻辑推理,编程等等,还能表达观点,玩游戏等.如果你有任何问题或需要帮助,欢迎随时告诉我!😊
**************************************************
我是DeepSeek Chat,由深度求索公司打造的AI助手!🤖✨ 我可以帮你回答问题,提供建议,聊天解闷,还能处理各种文本和文件信息.有什么我可以帮你的吗?😊
"""
