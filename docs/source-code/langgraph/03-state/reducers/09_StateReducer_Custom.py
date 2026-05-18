“””
【案例 03-9】自定义 Reducer：用函数签名 (current, update) -> 合并结果，解决 operator.mul 首次规约边界问题

知识点速览：
- Reducer 可以是普通函数：接收 current 与 update，返回合并结果。
- 自定义 Reducer 的价值在于可按业务语义处理首次合并、空值、重复值等边界。
- 节点仍只返回增量，真正决定合并方式的是 Reducer。
“””

from typing import Annotated

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


def my_operator_mul(current: float, update: float) -> float:
    """自定义乘法 Reducer：首次合并时 current 为 0.0 需特殊处理。"""
    if current == 0.0:
        print(f"current:{current}")
        print(f"update:{update}")
        return 1.0 * update
    return current * update


class MultiplyState(TypedDict):
    factor: Annotated[float, my_operator_mul]


def multiplier(state: MultiplyState) -> dict:
    return {"factor": 2.0}


def run_demo():
    print("使用自定义reducer解决乘法问题:")
    builder = StateGraph(MultiplyState)
    builder.add_node("multiplier", multiplier)
    builder.add_edge(START, "multiplier")
    builder.add_edge("multiplier", END)
    graph = builder.compile()

    result = graph.invoke({"factor": 5.0})
    print(f"初始状态: {{'factor': 5.0}}")
    print(f"执行结果: {result}")
    print(f"解释: 5.0 * 2.0 = 10.0\n")


if __name__ == "__main__":
    run_demo()

"""
【输出示例】
使用自定义reducer解决乘法问题:
current:0.0
update:5.0
初始状态: {'factor': 5.0}
执行结果: {'factor': 10.0}
解释: 5.0 * 2.0 = 10.0
"""
