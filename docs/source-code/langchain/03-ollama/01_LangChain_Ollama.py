“””
【案例 03-1】LangChain + Ollama 本地大模型对话

对应教程章节：第 12 章 - Ollama 本地部署与调用 → 5、LangChain 整合 Ollama 调用本地大模型

知识点速览：
- ChatOllama 连接本机 Ollama 服务，无需云端 API Key
- base_url 指向本机服务（默认 http://localhost:11434），model 需与 ollama list 中的标签一致
- 返回值仍为 AIMessage，用法与云端模型一致
“””

from langchain_ollama import ChatOllama

# ========== 1. 初始化本地模型 ==========
model = ChatOllama(
    base_url=”http://localhost:11434”,
    model=”qwen:4b”,
    reasoning=False,  # 是否开启推理模式（取决于具体模型是否支持）
)

# ========== 2. 调用并打印回复 ==========
response = model.invoke(“什么是LangChain，100字以内回答”)
print(response)
# 只取正文：print(response.content)
