"""
【案例 10-1】用 TextLoader 加载纯文本（TXT）为 Document 列表

知识点速览：
- TextLoader 用于纯文本，需指定路径和编码，load() 返回 List[Document]
- 每个 Document 有 page_content（正文）和 metadata（如 source 路径）
- 加载后通常还需切块，再做向量化与入库
"""

# pip install langchain_community
from langchain_community.document_loaders import TextLoader

file_path = "assets/sample.txt"
encoding = "utf-8"

docs = TextLoader(file_path, encoding).load()

print(docs)
"""
【输出示例】
[Document(metadata={'source': 'assets/sample.txt'}, page_content='LangChain 是一个用于构建基于大语言模型（LLM）应用的开发框架……')]
"""
