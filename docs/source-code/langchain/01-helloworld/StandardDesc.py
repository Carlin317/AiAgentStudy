“””
【案例 01-5】工程化写法：用 LangChain 调用大模型（invoke + stream）

对应教程章节：第 10 章 - LangChain 快速上手与 HelloWorld → 6、实战：企业级封装与流式输出

知识点速览：
- invoke（一次性返回）与 stream（流式返回）两种调用方式
- 模型初始化封装为函数便于复用
- .env 管理密钥、logging 替代 print、try/except 分级异常处理

补充说明：
- 使用 ChatOpenAI 写法（0.x 风格）；1.x 统一入口见同目录 LangChainV1.0.py。
- 当前演示为”阿里百炼兼容端点 + DeepSeek 模型”，重点在工程化写法而非特定模型。
“””

# ========== 1. 导入与环境 ==========
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_core.exceptions import LangChainException

load_dotenv(encoding="utf-8")

# ========== 1.5. 日志配置 ==========
# 通过环境变量 LOG_LEVEL 控制日志级别（开发用 INFO，生产用 WARNING）
import logging

_log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, _log_level, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ========== 2. LLM 客户端初始化 ==========


def init_llm_client() -> ChatOpenAI:
    “””初始化 LLM 客户端，封装配置便于复用。”””
    api_key = os.getenv(“QWEN_API_KEY”)
    if not api_key:
        raise ValueError(“环境变量 QWEN_API_KEY 未配置，请检查 .env 文件”)

    llm = ChatOpenAI(
        model=”deepseek-v3.2”,
        api_key=api_key,
        base_url=”https://dashscope.aliyuncs.com/compatible-mode/v1”,
        temperature=0.7,  # 0 更确定，1 更随机
        max_tokens=2048,
    )
    return llm


# ========== 3. 主逻辑：invoke + stream 两种调用方式 ==========


def main():
    """主函数：演示 invoke 与 stream 调用，包含分级异常处理。"""
    try:
        llm = init_llm_client()
        logger.info("LLM客户端初始化成功")

        # invoke：同步调用，等模型全部答完后一次性返回，适合短问答
        question = "你是谁"
        response = llm.invoke(question)
        logger.info(f"问题：{question}")
        logger.info(f"回答：{response.content}")

        # stream：流式调用，逐 chunk 返回，适合长文或实时展示
        print("==================== 以下是流式输出（另一种调用方式）")
        print("*" * 50)
        response_stream = llm.stream("介绍下 langchain，300字以内")
        for chunk in response_stream:
            print(chunk.content, end="")
        print()

    except ValueError as e:
        logger.error(f"配置错误：{str(e)}")
    except LangChainException as e:
        logger.error(f"模型调用失败：{str(e)}")
    except Exception as e:
        logger.error(f"未知错误：{str(e)}")


# ========== 4. 脚本入口 ==========
if __name__ == "__main__":
    main()

"""
【输出示例】
2026-03-26 17:30:58,192 - INFO - LLM客户端初始化成功
2026-03-26 17:31:03,613 - INFO - HTTP Request: POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions "HTTP/1.1 200 OK"
2026-03-26 17:31:03,617 - INFO - 问题：你是谁
2026-03-26 17:31:03,617 - INFO - 回答：你好！我是DeepSeek，由深度求索公司创造的AI助手。😊

我是一个纯文本模型，可以帮你解答各种问题、进行对话、协助处理文档等。虽然我不支持多模态识别，但我具有文件上传功能，可以读取和处理图像、txt、pdf、ppt、word、excel等文件中的文字信息。

我的知识截止到2024年7月，拥有128K的上下文处理能力，而且完全免费使用！如果需要最新信息，你可以手动开启联网搜索功能。

有什么我可以帮助你的吗？无论是学习、工作还是日常问题，我都很乐意为你提供帮助！✨
==================== 以下是流式输出（另一种调用方式）
**************************************************
2026-03-26 17:31:04,798 - INFO - HTTP Request: POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions "HTTP/1.1 200 OK"
LangChain 是一个用于开发大语言模型（LLM）应用的开源框架。它核心解决了LLM应用中的两大问题：**数据实时性**（LLM训练数据可能过时）和**领域局限性**（缺乏特定领域知识）。

其核心思想是通过“链”式设计，将LLM与外部数据源和工具连接起来，构建功能更强的应用。主要组件包括：
*   **模型**：兼容多种LLM（如GPT、Claude等）。
*   **提示模板**：管理并优化与LLM的交互提示。
*   **数据检索**：能从外部文档、数据库、网络等获取实时信息。
*   **链**：将多个组件按顺序组合，完成复杂任务（如问答、摘要）。
*   **代理**：让LLM自主选择调用工具（如计算器、搜索引擎）来完成任务。

简而言之，LangChain如同“乐高积木”，帮助开发者快速搭建基于LLM的智能应用，如知识库问答、文档分析、智能客服等，极大地提升了开发效率。
"""
