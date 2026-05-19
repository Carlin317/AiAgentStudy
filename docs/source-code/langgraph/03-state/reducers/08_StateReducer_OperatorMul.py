"""
[案例 03-8]operator.mul 作为 Reducer 的"陷阱"演示:float 默认值 0.0 导致首次规约为 0,后续乘法始终为 0

知识点速览:
- 重点是理解对初始值敏感的规约逻辑,不能只看 reducer 函数名,还要看首次合并边界.
- 字段默认值 0.0 时,0.0 * 初始值 = 0.0,后续无法恢复.
- 解决方式:改用自定义 Reducer 显式处理首次合并逻辑,参见 StateReducer_Custom.py.
"""

import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class MultiplyState(TypedDict):
    factor: Annotated[float, operator.mul]


def multiplier(state: MultiplyState) -> dict:
    return {"factor": 2.0}


# 故意保留 operator.mul 的"踩坑版"写法,对照 StateReducer_Custom.py 理解自定义 Reducer 的价值


def run_demo():
    print("4. operator.mul Reducer(数值相乘)演示:")
    builder = StateGraph(MultiplyState)
    builder.add_node("multiplier", multiplier)
    builder.add_edge(START, "multiplier")
    builder.add_edge("multiplier", END)
    graph = builder.compile()

    result = graph.invoke({"factor": 5.0})
    print(f"初始状态: {{'factor': 5.0}}")
    print(f"执行结果: {result}")
    print(
        "说明: 因 float 默认 0.0 先参与规约,0.0 * 5.0 = 0.0,后续乘 2.0 仍为 0.0;乘法场景请用自定义 Reducer.\n"
    )


if __name__ == "__main__":
    run_demo()

"""
[输出示例]
4. operator.mul Reducer(数值相乘)演示:
初始状态: {'factor': 5.0}
执行结果: {'factor': 0.0}
说明: 因 float 默认 0.0 先参与规约,0.0 * 5.0 = 0.0,后续乘 2.0 仍为 0.0;乘法场景请用自定义 Reducer.
"""
