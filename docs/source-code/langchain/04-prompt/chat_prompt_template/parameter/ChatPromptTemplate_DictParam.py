“””
【案例 04-19】用「字典」定义 ChatPromptTemplate 的消息

对应教程章节：第 13 章 - 提示词与消息模板 → 7、对话提示词模板（ChatPromptTemplate）

知识点速览：
- 字典写法最贴近 OpenAI 风格：{“role”: “...”, “content”: “...”}
- 适合与 JSON 配置、接口透传数据等场景对齐
“””

from langchain_core.prompts import ChatPromptTemplate

# ========== 1. from_messages ==========
chat_prompt = ChatPromptTemplate.from_messages(
    [
        {"role": "system", "content": "你是AI助手，你的名字叫{name}。"},
        {"role": "user", "content": "请问：{question}"},
    ]
)
message = chat_prompt.format_messages(name="小问", question="什么是LangChain")
print("from_messages:", message)

# ========== 2. 构造函数（效果一致） ==========
chat_prompt2 = ChatPromptTemplate(
    [
        {"role": "system", "content": "你是AI助手，你的名字叫{name}。"},
        {"role": "user", "content": "请问：{question}"},
    ]
)
message2 = chat_prompt2.format_messages(name="小问", question="什么是LangChain")
print("构造函数:", message2)

"""
【输出示例】
[SystemMessage(content='你是AI助手，你的名字叫小问。', additional_kwargs={}, response_metadata={}), HumanMessage(content='请问：什么是LangChain', additional_kwargs={}, response_metadata={})]
"""
