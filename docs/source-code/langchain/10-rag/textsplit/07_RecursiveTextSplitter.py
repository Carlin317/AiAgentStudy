"""
【案例 10-7】用 RecursiveCharacterTextSplitter 分割纯文本

知识点速览：
- 大文档需先切块再向量化，控制 token 成本并提高检索精度
- RecursiveCharacterTextSplitter 按字符递归切分，尽量保持语义完整
- chunk_size：单块最大长度；chunk_overlap：相邻块重叠字符数（常用 10%~20%）
- split_text() 返回字符串列表；create_documents() 将其转为 Document 列表
- 重叠使总字符数大于原文，这是为了减少截断问题，不是 bug
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

# ========== 1. 待分割的原文 ==========
content = (
    "大模型RAG（检索增强生成）是一种结合生成模型与外部知识检索的技术，通过从大规模文档或数据库中检索相关信息，"
    "辅助生成模型以提升回答的准确性和相关性。其核心流程包括用户输入查询、系统检索相关知识、"
    "生成模型基于检索结果生成内容，并输出最终答案。RAG的优势在于能够弥补生成模型的知识盲区，"
    "提供更准确、实时和可解释的输出，广泛应用于问答系统、内容生成、客服、教育和企业领域。"
    "然而，其也面临依赖高质量知识库、可能的响应延迟、较高的维护成本以及数据隐私等挑战。"
)

# ========== 2. 配置分割器 ==========
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100, chunk_overlap=30, length_function=len
)

# ========== 3. 切成字符串列表，再转 Document 列表 ==========
splitter_texts = text_splitter.split_text(content)
splitter_documents = text_splitter.create_documents(splitter_texts)

print(f"原始文本大小：{len(content)}")
print(f"分割文档数量：{len(splitter_documents)}")
for splitter_document in splitter_documents:
    print(
        f"文档片段大小：{len(splitter_document.page_content)},文档内容：{splitter_document.page_content}"
    )

"""
【输出示例】
原始文本大小：225
分割文档数量：3
文档片段大小：100,文档内容：大模型RAG（检索增强生成）……
文档片段大小：100,文档内容：相关性。其核心流程……
文档片段大小：85,文档内容：区，提供更准确……

100+100+85=285，比原始 225 多 60，因为两处 chunk_overlap=30 各重复了 30 字符：
285 - 60 = 225，与原文一致，无丢失。
"""
