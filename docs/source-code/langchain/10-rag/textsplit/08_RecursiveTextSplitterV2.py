"""
【案例 10-8】RecursiveCharacterTextSplitter 分割验证：剔除重叠后拼接校验完整性

知识点速览：
- 与 10-7 使用相同分割参数，侧重验证 chunk_overlap 不会造成内容丢失
- split_text() 后手动转 Document：显式展示"字符串块 -> Document"这一步
- 剔除重叠部分再拼接，可验证是否完整覆盖原文
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

content = (
    "大模型RAG（检索增强生成）是一种结合生成模型与外部知识检索的技术，通过从大规模文档或数据库中检索相关信息，"
    "辅助生成模型以提升回答的准确性和相关性。其核心流程包括用户输入查询、系统检索相关知识、"
    "生成模型基于检索结果生成内容，并输出最终答案。RAG的优势在于能够弥补生成模型的知识盲区，"
    "提供更准确、实时和可解释的输出，广泛应用于问答系统、内容生成、客服、教育和企业领域。"
    "然而，其也面临依赖高质量知识库、可能的响应延迟、较高的维护成本以及数据隐私等挑战。"
)

# ========== 1. 分割文本 ==========
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100, chunk_overlap=30, length_function=len
)

splitter_texts = text_splitter.split_text(content)
splitter_documents = [Document(page_content=text) for text in splitter_texts]

# ========== 2. 剔除重叠后拼接验证 ==========
full_content = ""
for text in splitter_texts:
    if full_content:
        full_content += text[30:]  # 跳过与前一块重叠的 30 字符
    else:
        full_content += text

print(f"原始文本大小：{len(content)}，原始内容：\n{content}\n")
print(f"分割文档数量：{len(splitter_documents)}\n")
for idx, splitter_document in enumerate(splitter_documents, 1):
    print(
        f"第{idx}个文档 - 大小：{len(splitter_document.page_content)}, 内容：{splitter_document.page_content}\n"
    )

print(f"拼接后文本大小：{len(full_content)}")
print(f"是否与原始文本完全一致：{full_content == content}")
print(f"拼接后完整内容：\n{full_content}")
