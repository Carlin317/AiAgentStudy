"""
[案例 04-18]用"Message 类"定义 ChatPromptTemplate 的消息

对应教程章节:第 13 章 - 提示词与消息模板 → 7,对话提示词模板(ChatPromptTemplate)

知识点速览:
- SystemMessage / HumanMessage / AIMessage 是最直观的消息表示
- 角色语义一眼可见,且可扩展工具调用,元数据等
"""

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate(
    [
        SystemMessage(content="你是AI助手,你的名字叫{name}."),
        HumanMessage(content="请问:{question}"),
    ]
)

message = chat_prompt.format_messages(name="亮仔", question="什么是LangChain")
print(message)

"""
[输出示例]
[SystemMessage(content='你是AI助手,你的名字叫亮仔.', additional_kwargs={}, response_metadata={}), HumanMessage(content='请问:什么是LangChain', additional_kwargs={}, response_metadata={})]
"""
