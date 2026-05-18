"""
【案例 04-16】from_messages 创建模板 + format_messages / invoke / format 的用法

对应教程章节：第 13 章 - 提示词与消息模板 → 7、对话提示词模板（ChatPromptTemplate）

知识点速览：
- from_messages 是创建 ChatPromptTemplate 的主流写法
- format_messages 返回消息列表，invoke 返回 ChatPromptValue，format 返回字符串
- 发给聊天模型时优先用 format_messages 或 invoke，保留角色结构
"""

from langchain_core.prompts import ChatPromptTemplate

# 用 from_messages 创建模板：一条 system（带 {role}）、一条 human（带 {question}）
chat_prompt = ChatPromptTemplate.from_messages(
    [("system", "你是一个{role}，请回答我提出的问题"), ("human", "请回答:{question}")]
)

# ========== 1. format_messages ==========
prompt_value = chat_prompt.format_messages(
    **{"role": "python开发工程师", "question": "堆排序怎么写"}
)
print(prompt_value)

print()
# ========== 2. invoke（返回 ChatPromptValue） ==========
prompt_value2 = chat_prompt.invoke(
    {"role": "python开发工程师", "question": "堆排序怎么写"}
)
print(prompt_value2.to_string())

print()

# ========== 3. format（返回字符串） ==========
prompt_value3 = chat_prompt.format(
    **{"role": "python开发工程师", "question": "快速排序怎么写"}
)
print(prompt_value3)

"""
【输出示例】
[SystemMessage(content='你是一个python开发工程师，请回答我提出的问题', additional_kwargs={}, response_metadata={}), HumanMessage(content='请回答:堆排序怎么写', additional_kwargs={}, response_metadata={})]

System: 你是一个python开发工程师，请回答我提出的问题
Human: 请回答:堆排序怎么写

System: 你是一个python开发工程师，请回答我提出的问题
Human: 请回答:快速排序怎么写
"""
