"""
[案例 04-5]模型调用:异步 ainvoke

对应教程章节:第 13 章 - 提示词与消息模板 → 4,调用大模型的调用方式

知识点速览:
- ainvoke 是 invoke 的异步版本,等待模型返回时不阻塞事件循环
- 适合异步 Web 服务,并发任务等场景
- 返回值仍为 AIMessage,调用方式变为 await
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# ========== 1. 实例化模型 ==========
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


async def main():
    """异步主函数:用 await 调用 ainvoke."""
    # ========== 2. 异步调用 ==========
    response = await model.ainvoke("解释一下LangChain是什么,简洁回答100字以内")
    print(f"响应类型:{type(response)}")
    print(response.content_blocks)


# ========== 3. 运行异步程序 ==========
if __name__ == "__main__":
    asyncio.run(main())

"""
[输出示例]
响应类型:<class 'langchain_core.messages.ai.AIMessage'>
[{'type': 'text', 'text': 'LangChain是一个开源框架,用于构建基于大语言模型(LLM)的应用程序.它提供模块化组件(如链,代理,记忆,工具集成等),支持提示工程,数据检索增强(RAG),多步推理和外部工具调用,简化LLM应用的开发,编排与部署.'}]
"""
