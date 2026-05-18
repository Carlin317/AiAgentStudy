"""
【案例 05-2】Python 基础：Pydantic + Annotated 实现带范围的运行时校验

对应教程章节：第 14 章 - 输出解析器 → 3、结构化输出（TypedDict / Pydantic / Annotated）

知识点速览：
- Pydantic 的 Field(ge=0, le=150) 配合 Annotated，可在运行时校验数值范围
- 与 AnnotatedTypedDict.py 的区别：TypedDict 的 Annotated 只是元数据，不做校验
- LangChain 的结构化输出也可用 Pydantic 模型做解析与校验
"""

from typing import Annotated
from pydantic import BaseModel, Field, ValidationError

# Annotated + Field：ge=0, le=150 会在运行时触发 Pydantic 校验
Age = Annotated[int, Field(ge=0, le=150, description="年龄，范围0-150")]


class Person(BaseModel):
    name: str
    age: int
    age2: Age


try:
    p = Person(name="z3", age=11, age2=188)  # age2=188 超出范围，抛 ValidationError
    print(p)
except ValidationError as e:
    print("数据校验失败：")
    print(e)

"""
【输出示例】
数据校验失败：
1 validation error for Person
age2
  Input should be less than or equal to 150 [type=less_than_equal, input_value=188, input_type=int]
    For further information visit https://errors.pydantic.dev/2.12/v/less_than_equal
"""
