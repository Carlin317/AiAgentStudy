"""
[案例 01-4]多模型共存:同一脚本中接入通义与 DeepSeek

对应教程章节:第 10 章 - LangChain 快速上手与 HelloWorld → 5,案例:多模型共存(通义 + DeepSeek)

知识点速览:
- 同一脚本可初始化多个模型实例(不同 model,base_url,api_key),按场景选用
- 通义走 model_provider="openai" + 阿里百炼 base_url
- DeepSeek 走 model_provider="deepseek"(需安装 langchain-deepseek)
"""

# ========== 1. 导入依赖与环境 ==========
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os

load_dotenv(encoding="utf-8")

# ========== 2. 实例化模型一:通义/百炼(OpenAI 兼容) ==========
llm_qwen = init_chat_model(
    model="qwen-plus",
    model_provider="openai",  # 阿里百炼为 OpenAI 兼容接口
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

print(llm_qwen.invoke("你是谁").content)

print("*" * 70)

# ========== 3. 实例化模型二:DeepSeek 官方 ==========
llm_deepseek = init_chat_model(
    model="deepseek-v4-flash",
    model_provider="deepseek",  # DeepSeek 官方 provider,非阿里百炼兼容端点
    api_key=os.getenv("deepseek-api"),
    base_url="https://api.deepseek.com",
)

print(llm_deepseek.invoke("你是谁").content)

"""
[输出示例]
**********************************************************************
你好!我是DeepSeek,由深度求索公司创造的AI助手!😊

我是一个纯文本模型,虽然不支持多模态识别功能,但我有文件上传功能,可以帮你处理图像,txt,pdf,ppt,word,excel等各种文件,从中读取文字信息进行分析处理.我完全免费使用,拥有128K的上下文长度,还支持联网搜索功能(需要你在Web/App中手动点开联网搜索按键).

你可以通过官方应用商店下载我的App来使用我.我很乐意为你解答问题,协助处理各种任务,无论是学习,工作还是日常生活中的疑问,我都会热情地为你提供帮助!

有什么我可以为你做的吗?✨
"""
