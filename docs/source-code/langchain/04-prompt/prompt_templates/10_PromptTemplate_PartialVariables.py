“””
【案例 04-10】文本提示词模板：partial_variables 与 partial()

对应教程章节：第 13 章 - 提示词与消息模板 → 6、文本提示词模板（PromptTemplate）

知识点速览：
- partial_variables：创建模板时固定部分变量
- partial()：对已有模板再固定部分变量，返回新模板
- 适合沉淀稳定角色、固定规则、时间戳等公共上下文
“””

from langchain_core.prompts import PromptTemplate
from datetime import datetime
import time

# ========== 1. 创建时用 partial_variables 固定「时间」 ==========
template1 = PromptTemplate(
    template="现在时间是：{time},请对我的问题给出答案，我的问题是：{question}",
    input_variables=["question"],
    partial_variables={"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
)
# 写法二（等价）：from_template(..., partial_variables={...})
# template1 = PromptTemplate.from_template(
#     "现在时间是：{time},请对我的问题给出答案，我的问题是：{question}",
#     partial_variables={"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# )
prompt1 = template1.format(question="今天是几号？")
print(prompt1)

time.sleep(2)

# ========== 2. 用 partial() 方法固定部分变量 ==========
template2 = PromptTemplate.from_template(
    "现在时间是：{time},请对我的问题给出答案，我的问题是：{question}"
)
partial = template2.partial(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
prompt2 = partial.format(question="今天是几号？")
print(prompt2)

# ========== 3. format 时传入同名变量会覆盖 partial_variables ==========
template3 = PromptTemplate(
    template="{foo} {bar}",
    input_variables=["foo", "bar"],
    partial_variables={"foo": "hello"},
)
print(template3.format(foo="li4", bar="world"))  # li4 world
print(template3.format(bar="world"))  # hello world

"""
【输出示例】
现在时间是：2026-02-25 15:30:59,请对我的问题给出答案，我的问题是：今天是几号？
现在时间是：2026-02-25 15:31:01,请对我的问题给出答案，我的问题是：今天是几号？
li4 world
hello world
"""
