"""
【案例 10-4】用 UnstructuredMarkdownLoader 加载 Markdown 为 Document 列表

知识点速览：
- Markdown 天然带标题、列表、段落等结构，适合做知识库文档
- mode="elements" 按标题/段落等元素拆成多个 Document，保留结构
- 后续可选用 MarkdownHeaderTextSplitter 按标题切分
"""

# pip install langchain_community unstructured[md]
from langchain_community.document_loaders import UnstructuredMarkdownLoader

docs = UnstructuredMarkdownLoader(
    file_path="assets/sample.md",
    mode="elements",
).load()

print(docs)
"""
【输出示例】
[Document(metadata={'source': 'assets/sample.md', 'category': 'Title', ...}, page_content='投机解码（Speculative Decoding）介绍'), ...]
"""
