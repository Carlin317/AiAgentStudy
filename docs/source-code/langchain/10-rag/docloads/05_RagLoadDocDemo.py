"""
【案例 10-5】用 UnstructuredWordDocumentLoader 加载 Word（.docx）为 Document 列表

知识点速览：
- mode 可选 single（整篇一个 Document）或 elements（按标题等元素切分）
- Word 中"视觉上像标题"不一定能被稳定识别，取决于样式规范程度
- 需单独安装 unstructured：pip install unstructured[docx]
"""

# pip install langchain_community unstructured[docx] python-docx
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

docs = UnstructuredWordDocumentLoader(
    file_path="assets/alibaba-more.docx",
    mode="single",
).load()

print(docs)
"""
【输出示例】
[Document(metadata={'source': 'assets/alibaba-more.docx'}, page_content='Java开发手册（黄山版）\n\n...')]
"""
