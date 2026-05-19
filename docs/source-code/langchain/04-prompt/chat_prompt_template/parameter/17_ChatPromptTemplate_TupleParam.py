"""
[案例 04-17]用"元组 (role, content)"定义 ChatPromptTemplate 的消息

对应教程章节:第 13 章 - 提示词与消息模板 → 7,对话提示词模板(ChatPromptTemplate)

知识点速览:
- 元组写法 ("角色", "内容") 是最简洁的参数形式
- 与字典,Message 类写法本质等价,仅表达风格不同
"""

from langchain_core.prompts import ChatPromptTemplate

chat_prompt_template = ChatPromptTemplate(
    [
        ("system", "你是一个AI开发工程师,你的名字是{name}."),
        ("human", "你能帮我做什么?"),
        ("ai", "我能开发很多{thing}."),
        ("human", "{user_input}"),
    ]
)

prompt = chat_prompt_template.format_messages(
    name="小谷AI", thing="AI", user_input="7 + 5等于多少"
)
print(prompt)

"""
[输出示例]
[SystemMessage(content='你是一个AI开发工程师,你的名字是小谷AI.', additional_kwargs={}, response_metadata={}), HumanMessage(content='你能帮我做什么?', additional_kwargs={}, response_metadata={}), AIMessage(content='我能开发很多AI.', additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[]), HumanMessage(content='7 + 5等于多少', additional_kwargs={}, response_metadata={})]
"""
