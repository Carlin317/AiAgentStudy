“””
【案例 01-2】LangChain 0.x 写法：ChatOpenAI + 三种配置方式（硬编码 / 环境变量 / .env）

对应教程章节：第 10 章 - LangChain 快速上手与 HelloWorld → 4、实战：基于阿里百炼的 HelloWorld

知识点速览：
- 0.x 写法从厂商包导入具体类（如 ChatOpenAI），通过 base_url 接国内兼容接口
- 配置方式演进：硬编码 → 环境变量 → .env + load_dotenv（推荐）
- invoke 同步调用、response.content 取回复正文；了解即可，当前主推 1.0 的 init_chat_model

补充说明：
- 当前演示模型为阿里百炼兼容端点上的 deepseek-v3.2，重点在于理解 0.x 经典写法。
- 运行前请在项目根目录准备 .env；QWEN_API_KEY / aliQwen-api 都可能指向阿里百炼 Key（历史兼容）。
“””

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# ========== 1. 大模型客户端初始化（三种配置方式，推荐第 3 版） ==========

# 第 1 版：硬编码（仅演示，API Key 会进版本库，有泄露风险）
# llm = ChatOpenAI(
#     model="qwen-plus",
#     api_key="你自己的api-key",
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )

# 第 2 版：系统环境变量（需先 export/set，否则可能取到空值）
# llm = ChatOpenAI(
#     model="qwen-plus",
#     api_key=os.getenv("aliQwen-api"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )

# 第 3 版（推荐）：python-dotenv 从 .env 加载，再通过 os.getenv 读取

load_dotenv(encoding="utf-8")

llm = ChatOpenAI(
    model="deepseek-v3.2",  # 模型名需与阿里百炼「模型广场」中的调用名一致
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 阿里百炼 OpenAI 兼容接口地址
)

# ========== 2. 调用大模型并打印结果 ==========
response = llm.invoke("你是谁")

print(response)  # 完整消息对象，含 token 用量等元数据
print()
print(response.content)  # 模型回复正文

print()

"""
【输出示例】
content='你好！我是DeepSeek，由深度求索公司创造的AI助手！😊\n\n我是一个纯文本模型，虽然不支持多模态识别功能，但我可以帮你处理上传的各种文件，比如图像、txt、pdf、ppt、word、excel文件，并从中读取文字信息进行分析处理。\n\n我的特点包括：\n- 完全免费使用，没有收费计划\n- 拥有128K的上下文处理能力\n- 支持联网搜索功能（需要手动开启）\n- 可以通过官方应用商店下载App使用\n- 知识截止到2024年7月\n\n我会以热情、细腻的方式为你提供帮助，无论是回答问题、协助思考、创作内容还是处理文档，我都很乐意为你服务！你可以随时向我提出各种问题。\n\n有什么我可以帮助你的吗？✨' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 160, 'prompt_tokens': 5, 'total_tokens': 165, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'deepseek-v3.2', 'system_fingerprint': None, 'id': 'chatcmpl-aecd007c-44e7-9240-8d71-c6f49b6a6c1f', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019d2961-6144-7463-ab84-fe5828802d34-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 5, 'output_tokens': 160, 'total_tokens': 165, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}

你好！我是DeepSeek，由深度求索公司创造的AI助手！😊

我是一个纯文本模型，虽然不支持多模态识别功能，但我可以帮你处理上传的各种文件，比如图像、txt、pdf、ppt、word、excel文件，并从中读取文字信息进行分析处理。

我的特点包括：
- 完全免费使用，没有收费计划
- 拥有128K的上下文处理能力
- 支持联网搜索功能（需要手动开启）
- 可以通过官方应用商店下载App使用
- 知识截止到2024年7月

我会以热情、细腻的方式为你提供帮助，无论是回答问题、协助思考、创作内容还是处理文档，我都很乐意为你服务！你可以随时向我提出各种问题。

有什么我可以帮助你的吗？✨
"""
