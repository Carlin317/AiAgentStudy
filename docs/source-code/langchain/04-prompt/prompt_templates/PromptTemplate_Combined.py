“””
【案例 04-11】文本提示词模板：组合多个 PromptTemplate

对应教程章节：第 13 章 - 提示词与消息模板 → 6、文本提示词模板（PromptTemplate）

知识点速览：
- 多个 PromptTemplate 可通过 + 组合，适合拆分”角色 / 规则 / 任务”分别维护
- 组合后仍为模板对象，format 时需传入所有占位符变量
“””

from langchain_core.prompts import PromptTemplate

# ========== 1. 模板 + 字符串拼接 ==========
template1 = (
    PromptTemplate.from_template("请用一句话介绍{topic}，要求通俗易懂\n")
    + "内容不超过{length}个字"
)
prompt1 = template1.format(topic="LangChain", length=100)
print(prompt1)

# ========== 2. 两个独立模板相加 ==========
prompt_a = PromptTemplate.from_template("请用一句话介绍{topic}，要求通俗易懂\n")
prompt_b = PromptTemplate.from_template("内容不超过{length}个字")
prompt_all = prompt_a + prompt_b
prompt2 = prompt_all.format(topic="LangChain", length=200)
print(prompt2)

"""
【输出示例】
请用一句话介绍LangChain，要求通俗易懂
内容不超过100个字
请用一句话介绍LangChain，要求通俗易懂
内容不超过200个字
"""
