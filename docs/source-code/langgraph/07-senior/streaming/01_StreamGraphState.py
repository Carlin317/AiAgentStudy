"""
[案例 07-1]流式传输图状态:对比 stream_mode 为 updates 与 values 时,每一步推送的内容差异.

对应教程章节:第 25 章 - LangGraph 高级特性 → 1,流式处理(Streaming)

知识点速览:
- stream_mode="updates":每步只推送本节点的增量更新.
- stream_mode="values":每步推送当前完整状态快照.
- 同一张图,换流模式即可获得不同的数据视角.
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class DiliState(TypedDict):
    topic: str
    joke: str


def refine_topic(state: DiliState):
    return {"topic": state["topic"] + " and cats"}


def generate_joke(state: DiliState):
    return {"joke": f"This is a joke about {state['topic']}"}


def main():
    graph = (
        StateGraph(DiliState)
        .add_node(refine_topic)
        .add_node(generate_joke)
        .add_edge(START, "refine_topic")
        .add_edge("refine_topic", "generate_joke")
        .add_edge("generate_joke", END)
        .compile()
    )

    # ========== 1. updates 模式 ==========
    for chunk in graph.stream({"topic": "ice cream"}, stream_mode="updates"):
        print(chunk)

    print()

    # ========== 2. values 模式 ==========
    for chunk in graph.stream({"topic": "ice cream"}, stream_mode="values"):
        print(chunk)


if __name__ == "__main__":
    main()
"""
[输出示例]
{'refine_topic': {'topic': 'ice cream and cats'}}
{'generate_joke': {'joke': 'This is a joke about ice cream and cats'}}

{'topic': 'ice cream'}
{'topic': 'ice cream and cats'}
{'topic': 'ice cream and cats', 'joke': 'This is a joke about ice cream and cats'}
"""
