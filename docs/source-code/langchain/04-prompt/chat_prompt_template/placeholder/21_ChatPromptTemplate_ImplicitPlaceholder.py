"""
[案例 04-21]隐式使用 MessagesPlaceholder:("placeholder", "{变量名}") 简写

对应教程章节:第 13 章 - 提示词与消息模板 → 7.5,MessagesPlaceholder:消息占位符

知识点速览:
- ("placeholder", "{memory}") 是 MessagesPlaceholder("memory") 的简写
- 让整份模板保持元组风格,写起来更短
"""

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个资深的Python应用开发工程师,请认真回答我提出的Python相关的问题",
        ),
        ("placeholder", "{memory}"),
        ("human", "{question}"),
    ]
)

prompt_value = prompt.invoke(
    {
        "memory": [
            HumanMessage("我的名字叫亮仔,是一名程序员"),
            AIMessage("好的,亮仔你好"),
        ],
        "question": "请问我的名字叫什么?",
    }
)
print(prompt_value.to_string())

"""
[输出示例]
System: 你是一个资深的Python应用开发工程师,请认真回答我提出的Python相关的问题
Human: 我的名字叫亮仔,是一名程序员
AI: 好的,亮仔你好
Human: 请问我的名字叫什么?
"""
