"""
[案例 10-6]用 PyPDFLoader 加载 PDF 为 Document 列表

知识点速览:
- PyPDFLoader 支持本地路径或 URL,extraction_mode 可选 plain(纯文本)或 layout(按版面)
- 每页对应一个 Document,metadata 中带页码,便于定位来源
- PDF 解析结构未必适合直接做 RAG,实际项目常需后续切块和清洗
- 需单独安装 pypdf:PyPDFLoader 内部按需 import pypdf
"""

# pip install langchain_community pypdf
from langchain_community.document_loaders import PyPDFLoader

docs = PyPDFLoader(
    file_path="assets/sample.pdf",
    extraction_mode="plain",
).load()

print(docs)
"""
[输出示例]
[Document(metadata={'source': 'assets/sample.pdf', 'total_pages': 36, 'page': 0, ...}, page_content='中国科学院国家天文台 \n2023 年部门预算'), ...]
"""
