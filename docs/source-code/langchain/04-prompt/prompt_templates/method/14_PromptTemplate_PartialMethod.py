"""
【案例 04-14】PromptTemplate 的 partial() 方法

对应教程章节：第 13 章 - 提示词与消息模板 → 6、文本提示词模板（PromptTemplate）

知识点速览：
- partial() 返回新模板，原模板不被修改
- 适合先固定角色/规则等稳定变量，再多次填充变化部分
"""

from langchain_core.prompts import PromptTemplate

# ========== 1. 创建带两个占位符的模板 ==========
template = PromptTemplate.from_template(
    "你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}"
)

# ========== 2. partial 固定 role，得到新模板 ==========
partial = template.partial(role="python开发")
print(partial)
print(type(partial))
print()

# ========== 3. 对新模板 format ==========
prompt = partial.format(question="冒泡排序怎么写？")
print(prompt)
print(type(prompt))

"""
【输出示例】
input_variables=['question'] input_types={} partial_variables={'role': 'python开发'} template='你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}'
<class 'langchain_core.prompts.prompt.PromptTemplate'>

# 你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：冒泡排序怎么写？
# <class 'str'>
"""
