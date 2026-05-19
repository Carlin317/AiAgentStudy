"""
[案例 04-8]文本提示词模板:from_template 创建 PromptTemplate

对应教程章节:第 13 章 - 提示词与消息模板 → 6,文本提示词模板(PromptTemplate)

知识点速览:
- from_template 自动从字符串中识别占位符变量,快捷创建模板
- format(...) 填入变量后得到字符串,可直接传给 model.invoke()
"""

from langchain_core.prompts import PromptTemplate

# ========== 1. 用 from_template 创建模板 ==========
template = PromptTemplate.from_template(
    "你是一个专业的{role}工程师,请回答我的问题给出回答,我的问题是:{question}"
)

# ========== 2. format 填入变量 ==========
prompt = template.format(role="python开发", question="快速排序怎么写?")
print(prompt)
print("\n\n")

# ========== 3. 另一个示例 ==========
template = PromptTemplate.from_template("请给我一个关于{topic}的{type}解释.")
prompt = template.format(topic="量子力学", type="详细")
print(prompt)
print(type(prompt))  # str

"""
[输出示例]
你是一个专业的python开发工程师,请回答我的问题给出回答,我的问题是:快速排序怎么写?



请给我一个关于量子力学的详细解释.
<class 'str'>
"""
