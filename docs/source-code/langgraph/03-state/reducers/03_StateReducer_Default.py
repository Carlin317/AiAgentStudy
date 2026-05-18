"""
【案例 03-3】默认 Reducer（覆盖更新）：未指定 Reducer 时，节点返回的值直接覆盖该字段

知识点速览：
- Reducer 决定「节点返回的更新如何合并到当前状态」；不指定时默认覆盖。
- 多节点依次更新同一字段时，最终只保留最后一个节点返回的值。
- 若需追加、累加等语义，需使用 add_messages、operator.add 等 Reducer。
"""

from typing import List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# 未指定 Reducer，默认覆盖更新
class DefaultReducerState(TypedDict):
    foo: int
    bar: List[str]


def node_default_1(state: DefaultReducerState) -> dict:
    print(state["foo"])
    print(state["bar"])
    return {"foo": 22}


def node_default_2(state: DefaultReducerState) -> dict:
    print(state["foo"])
    print(state["bar"])
    return {"bar": ["bye1", "bye2", "bye3"]}


def main():
    print("1. 默认 Reducer（覆盖更新）演示:\n")
    builder = StateGraph(DefaultReducerState)
    builder.add_node("node1", node_default_1)
    builder.add_node("node2", node_default_2)
    builder.add_edge(START, "node1")
    builder.add_edge("node1", "node2")
    builder.add_edge("node2", END)
    graph = builder.compile()

    result = graph.invoke(input={"foo": 1, "bar": ["hi"]})
    print(f"执行结果: {result}\n")


if __name__ == "__main__":
    main()

"""
【输出示例】
1. 默认 Reducer（覆盖更新）演示:

1
['hi']
22
['hi']
执行结果: {'foo': 22, 'bar': ['bye1', 'bye2', 'bye3']}
"""
