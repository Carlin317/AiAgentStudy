"""
[案例 04-13]PromptTemplate 的 invoke() 方法

对应教程章节:第 13 章 - 提示词与消息模板 → 6,文本提示词模板(PromptTemplate)

知识点速览:
- invoke() 返回 PromptValue(StringPromptValue),适合衔接链式调用
- .to_string() 得到字符串,.to_messages() 转为消息列表
"""

from langchain_core.prompts import PromptTemplate

# ========== 1. 创建模板 ==========
template = PromptTemplate.from_template(
    "你是一个专业的{role}工程师,请回答我的问题给出回答,我的问题是:{question}"
)

# ========== 2. invoke 传入变量,得到 PromptValue ==========
prompt = template.invoke({"role": "python开发", "question": "冒泡排序怎么写?"})
print(prompt)
print(type(prompt))
print()

# ========== 3. to_string() 得到字符串 ==========
print(prompt.to_string())
print(type(prompt.to_string()))
print()

# ========== 4. to_messages() 转为消息列表 ==========
print(prompt.to_messages())
print(type(prompt.to_messages()))


"""
[输出示例]
text='你是一个专业的python开发工程师,请回答我的问题给出回答,我的问题是:冒泡排序怎么写?'
<class 'langchain_core.prompt_values.StringPromptValue'>

你是一个专业的python开发工程师,请回答我的问题给出回答,我的问题是:冒泡排序怎么写?
<class 'str'>

[HumanMessage(content='你是一个专业的python开发工程师,请回答我的问题给出回答,我的问题是:冒泡排序怎么写?', additional_kwargs={}, response_metadata={})]
<class 'list'>
"""
