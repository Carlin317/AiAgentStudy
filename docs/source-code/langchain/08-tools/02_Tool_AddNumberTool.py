"""
【案例 08-2】基础加法工具：使用 @tool 装饰器将普通函数转为 LangChain Tool

对应教程章节：第 17 章 - Tools 工具调用 → 3、自定义 Tool → 3.1 @tool 装饰器 / 3.2 基础案例

知识点速览：
- @tool 将普通函数包装为 LangChain Tool，自动生成 name、description、args 等元信息
- 工具名默认为函数名，description 取自 docstring
- tool.invoke({...}) 是程序侧直接执行工具的写法，不等于模型自动调用
"""

from langchain_core.tools import tool


@tool
def add_number(a: int, b: int) -> int:
    """两个整数相加"""
    return a + b


# ========== 1. 直接执行工具 ==========
result = add_number.invoke({"a": 1, "b": 12})
print(result)

print()

# ========== 2. 查看工具元信息 ==========
print(f"{add_number.name=}\n{add_number.description=}\n{add_number.args=}")
