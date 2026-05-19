"""
[案例 08-1]Pydantic 基础:类型校验,自动转换与 ValidationError

对应教程章节:第 17 章 - Tools 工具调用 → 4,参数 schema:为什么要配合 Pydantic

知识点速览:
- Pydantic 在实例化时按类型注解做校验与转换:合法则自动转,不合法则抛 ValidationError
- StrictInt 拒绝自动转换,仅接受真实 int,适合需要更严格约束的场景
- 理解 Pydantic 校验机制有助于后续理解 Tool 的 args_schema
"""
from pydantic import BaseModel, ValidationError, StrictInt


class User(BaseModel):
    id: StrictInt  # 严格整数:不接受字符串,必须已是 int
    name: str
    age: int = 0  # 可选字段,默认 0


# ========== 1. 合法输入 ==========
try:
    u = User(id=42, name="z3")
except ValidationError as e:
    print(e)
print(u.id, type(u.id))  # 42 <class 'int'>

print()

# ========== 2. 非法输入 ==========
# id="abc" 不是 int,StrictInt 不做模糊转换,直接抛出 ValidationError
try:
    User(id="abc", name="Bob")
except ValidationError as e:
    print(e)
