"""
【案例 10-2】用 CSVLoader 加载 CSV 为 Document 列表

知识点速览：
- 不指定列时：整行拼成 page_content，metadata 仅含 source
- 指定 content_columns + metadata_columns 时：正文与元数据分离，便于检索时按字段过滤
- 检索只对 page_content 向量化，metadata 用于过滤和来源展示
"""

# pip install langchain_community
from langchain_community.document_loaders.csv_loader import CSVLoader

# ========== 1. 整行作为 page_content ==========
docs_all = CSVLoader(file_path="assets/sample.csv").load()
print("=== 方式一：整行作为 page_content ===")
print(
    "page_content 示例:",
    (
        docs_all[0].page_content[:80] + "..."
        if len(docs_all[0].page_content) > 80
        else docs_all[0].page_content
    ),
)
print("metadata 示例:", docs_all[0].metadata, "\n")

# ========== 2. 指定正文列与元数据列 ==========
docs_split = CSVLoader(
    file_path="assets/sample.csv",
    metadata_columns=["title", "author"],
    content_columns=["content"],
).load()
print("=== 方式二：content 列作为正文，title/author 进 metadata ===")
print("page_content 示例:", docs_split[0].page_content)
print("metadata 示例:", docs_split[0].metadata)


"""
【输出示例】
=== 方式一：整行作为 page_content ===
page_content 示例: id: 1
title: Introduction to Python
content: Python is a popular programming lan...
metadata 示例: {'source': 'assets/sample.csv', 'row': 0}

=== 方式二：content 列作为正文，title/author 进 metadata ===
page_content 示例: content: Python is a popular programming language.
metadata 示例: {'source': 'assets/sample.csv', 'row': 0, 'title': 'Introduction to Python', 'author': 'John Doe'}
"""
