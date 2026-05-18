“””
【案例 07-3】自定义流（custom）最简版：节点内通过 get_stream_writer() 写入任意可序列化数据，stream 侧用 custom 接收。

对应教程章节：第 25 章 - LangGraph 高级特性 → 1、流式处理（Streaming）

知识点速览：
- get_stream_writer() 仅在 stream/astream 执行过程中有效；stream_mode 须包含 “custom”。
- 自定义块与状态更新是两条独立通道：前者适合 UI/日志/进度提示，后者通过 State 和 Reducer 管理。
“””

from typing import TypedDict

from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    query: str
    answer: str


def node(state: State):
    writer = get_stream_writer()
    writer({"custom_key": "欢迎来到线上Agent班级学习，O(∩_∩)O"})
    return {"answer": "some data"}


def main():
    graph = (
        StateGraph(State)
        .add_node(node)
        .add_edge(START, "node")
        .add_edge("node", END)
        .compile()
    )

    for chunk in graph.stream({"query": "example"}, stream_mode=["values", "custom"]):
        print(chunk)


if __name__ == "__main__":
    main()

"""
【输出示例】
('values', {'query': 'example'})
('custom', {'custom_key': '欢迎来到线上Agent班级学习，O(∩_∩)O'})
('values', {'query': 'example', 'answer': 'some data'})
"""
