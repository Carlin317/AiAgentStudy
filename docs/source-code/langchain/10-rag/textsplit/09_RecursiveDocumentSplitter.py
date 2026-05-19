"""
[案例 10-9]对 Document 列表做分割:先加载再 split_documents

知识点速览:
- 实际 RAG 流程:加载器 load() -> Document 列表 -> split_documents() -> 更小的 Document 列表
- split_documents() 直接对 Document 列表切分,切出的块保留 metadata
- 为何用 split_documents 而非 split_text?入参是 Document 列表,需保留 metadata
"""

# pip install langchain-unstructured
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_unstructured import UnstructuredLoader

# ========== 1. 加载文档 ==========
loader = UnstructuredLoader("rag.txt")
documents = loader.load()

# ========== 2. 分割 ==========
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100, chunk_overlap=30, length_function=len
)

splitter_documents = text_splitter.split_documents(documents)

# ========== 3. 查看结果 ==========
print(f"分割文档数量:{len(splitter_documents)}")
for splitter_document in splitter_documents:
    print(f"文档片段:{splitter_document.page_content}")
    print(
        f"文档片段大小:{len(splitter_document.page_content)}, 文档元数据:{splitter_document.metadata}"
    )

"""
[输出示例]
分割文档数量:14
文档片段:<倚天屠龙记>是金庸"射雕三部曲"的终章……
文档片段大小:50, 文档元数据:{'source': 'rag.txt', ...}
……
"""
