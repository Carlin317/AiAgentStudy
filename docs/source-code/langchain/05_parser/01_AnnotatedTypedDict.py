"""
[案例 05-1]Python 基础:Annotated 与 TypedDict(仅类型提示,无运行时校验)

对应教程章节:第 14 章 - 输出解析器 → 3,结构化输出(TypedDict / Pydantic / Annotated)

知识点速览:
- Annotated[类型, "描述"] 中的描述只是元数据,供文档,类型检查或 LangChain 生成提示用
- Python 运行时不会按描述做校验,故 age2=188 不会报错
- 若需运行时范围校验,要用 Pydantic 的 Field(见 AnnotatedPydantic.py)
"""

from typing import Annotated, TypedDict

# Annotated 中的字符串只是元数据,运行时不会做 0-150 的校验
Age = Annotated[int, "年龄,范围0-150"]


class Person(TypedDict):
    name: str
    age: int
    age2: Age


# TypedDict 不做值校验,只要类型是 int 即可
p = Person(name="z3", age=111, age2=188)
print(p)

"""
[输出示例]
{'name': 'z3', 'age': 111, 'age2': 188}
"""
