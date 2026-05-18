“””
【案例 04-20】显式使用 MessagesPlaceholder：在模板里预留消息位置

对应教程章节：第 13 章 - 提示词与消息模板 → 7.5、MessagesPlaceholder：消息占位符

知识点速览：
- MessagesPlaceholder 在模板中预留”消息列表位置”，调用时整块插入历史对话
- 适合多轮对话、记忆、上下文拼接等场景
- 显式写法 MessagesPlaceholder(“memory”)，invoke 时键名须一致
“””

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            “system”,
            “你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题”,
        ),
        MessagesPlaceholder(“memory”),
        (“human”, “{question}”),
    ]
)

# 用两条消息模拟上一轮对话，测试模型是否利用上下文
prompt_value = prompt.invoke(
    {
        "memory": [
            HumanMessage("我的名字叫亮仔，是一名程序员111"),
            AIMessage("好的，亮仔你好222"),
        ],
        "question": "请问我的名字叫什么？",
    }
)

print(prompt_value.to_string())

"""
【输出示例】
System: 你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题
Human: 我的名字叫亮仔，是一名程序员111
AI: 好的，亮仔你好222
Human: 请问我的名字叫什么？
"""
