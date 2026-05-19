"""
[案例 10-3]用 JSONLoader 加载 JSON 文件为 Document 列表

知识点速览:
- jq_schema 指定提取路径(如 "." 整份,".key" 某字段);text_content 控制是否当文本处理
- "." 把整份 JSON 当一条内容,真实 RAG 中通常抽取更具体的字段或列表项
- 依赖 jq:pip install jq
"""

# pip install jq langchain_community
from langchain_community.document_loaders import JSONLoader

docs = JSONLoader(
    file_path="assets/sample.json",
    jq_schema=".",
    text_content=False,
).load()

print(docs)

"""
[输出示例]
[Document(metadata={'source': '.../sample.json', 'seq_num': 1}, page_content='{"status": "success", "data": {...}}')]
"""
