"""
[案例 03-1]最简 State 定义与"无中间节点"图:用 TypedDict 定义状态,构建 START → END 直连边

知识点速览:
- State 由 Schema(模式)和 Reducer(规约函数)两部分组成.
- TypedDict 定义 State Schema(字段名与类型);未用 Annotated[..., reducer] 时,默认覆盖旧值.
- add_edge(START, END) 表示无业务节点,状态原样透传.
- invoke() 核心位置参数是状态字典,可选第二参数为 config.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class BasicState(TypedDict):
    user_input: str
    response: str
    count: int
    process_data: dict


# ========== 1. 构建图 ==========
basic_state = StateGraph(BasicState)
basic_state.add_edge(START, END)
app = basic_state.compile()

# ========== 2. 执行 ==========
initial_state = {
    "user_input": "a",
    "response": "resp",
    "count": 25,
    "process_data": {"k1": "v1"},
}

result = app.invoke(initial_state)
print("执行结果:", result)

"""
[输出示例]
执行结果: {'user_input': 'a', 'response': 'resp', 'count': 25, 'process_data': {'k1': 'v1'}}
"""
