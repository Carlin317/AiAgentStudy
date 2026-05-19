"""
[案例 10-12]RAG 综合流程:加载 docx -> 分割 -> 向量化存 Redis -> 检索 -> 提示词模板 -> 大模型回答

知识点速览:
- 完整管道式 RAG:索引阶段(加载,切分,向量化,入库)+ 检索生成阶段(检索,拼 Prompt,调 LLM)
- 文档流入库路线:Loader + Splitter 得到 Document 列表,Redis.from_documents() 一步完成向量化与建索引
- RunnablePassthrough() 把用户问题同时传给 retriever(查询)和 prompt(作为 {question})
- 本例保留了"有 RAG / 无 RAG"对比,直观展示外挂知识库的价值
"""

# pip install unstructured docx2txt python-docx
from langchain.chat_models import init_chat_model
import os
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.prompts import PromptTemplate

# 注意:langchain_classic 为社区维护的兼容包,CharacterTextSplitter 在新版中
# 已迁移至 langchain_text_splitters.CharacterTextSplitter,建议优先使用新路径
from langchain_classic.text_splitter import CharacterTextSplitter

from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from dotenv import load_dotenv

load_dotenv()

# ========== 1. 初始化大模型 ==========
llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 2. 提示词模板 ==========
prompt_template = """
    请使用以下提供的文本内容来回答问题.仅使用提供的文本信息,
    如果文本中没有相关信息,请回答"抱歉,提供的文本中没有这个信息".

    文本内容:
    {context}

    问题:{question}

    回答:
"""
prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# ========== 3. 嵌入模型 ==========
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3", dashscope_api_key=os.getenv("aliQwen-api")
)

# ========== 4. 加载 docx ==========
loader = Docx2txtLoader("alibaba-java.docx")
documents = loader.load()

# ========== 5. 分割 ==========
# CharacterTextSplitter 便于快速跑通;真实项目更常用 RecursiveCharacterTextSplitter
text_splitter = CharacterTextSplitter(
    chunk_size=1000, chunk_overlap=0, length_function=len
)
texts = text_splitter.split_documents(documents)

print(f"文档个数:{len(texts)}")

# ========== 6. 向量化并写入 Redis ==========
vector_store = Redis.from_documents(
    documents=texts,
    embedding=embeddings,
    redis_url="redis://localhost:26379",
    index_name="my_index3",
)

# ========== 7. 检索器 ==========
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# ========== 8. LCEL 链:question -> context(retriever) + question(直通) -> prompt -> llm ==========
rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

# ========== 9. 有 RAG 的回答 ==========
question = "00000和A0001分别是什么意思"
result = rag_chain.invoke(question)
print("\n=== 有外挂知识库(RAG:从 alibaba-java.docx 检索)===")
print("问题:", question)
print("回答:", result.content)

# ========== 10. 对比:无 RAG ==========
no_rag_chain = (
    {
        "context": lambda _: "(未提供相关文档,模拟无外挂知识库)",
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
)
result_no_rag = no_rag_chain.invoke(question)
print("\n=== 无外挂知识库(模拟:不检索,仅靠模型自身知识)===")
print("问题:", question)
print("回答:", result_no_rag.content)

"""
[输出示例]
=== 有外挂知识库 ===
回答: 00000 的意思是"一切 ok";A0001 的意思是"用户端错误",属于一级宏观错误码.

=== 无外挂知识库 ===
回答: 抱歉,提供的文本中没有这个信息
"""
