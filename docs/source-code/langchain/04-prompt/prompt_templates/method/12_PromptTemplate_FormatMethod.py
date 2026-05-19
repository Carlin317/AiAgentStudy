"""
[案例 04-12]PromptTemplate 的 format() 方法

对应教程章节:第 13 章 - 提示词与消息模板 → 6,文本提示词模板(PromptTemplate)

知识点速览:
- format() 填入变量后直接得到字符串
- 未传入的占位符会报错,帮助尽早发现参数遗漏
"""

from langchain_core.prompts import PromptTemplate

# ========== 1. 创建模板 ==========
template = PromptTemplate.from_template(
    "你是一个专业的{role}工程师,请回答我的问题给出回答,我的问题是:{question}"
)

# ========== 2. format 填入变量 ==========
prompt = template.format(role="python开发", question="二分查找算法怎么写?")
print(prompt)
print(type(prompt))  # str

"""
[输出示例]
你是一个专业的python开发工程师,请回答我的问题给出回答,我的问题是:二分查找算法怎么写?
<class 'str'>
"""
