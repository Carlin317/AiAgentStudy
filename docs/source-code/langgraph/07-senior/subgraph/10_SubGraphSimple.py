“””
【案例 07-10】父子图共享字段：父图与子图 State 均含 parent_messages；
子图私有字段不会出现在父图最终 state（父 schema 未声明）。

对应教程章节：第 25 章 - LangGraph 高级特性 → 4、子图（Subgraphs）

知识点速览：
- 子图 compile 后作为父图的一个 node；父图 invoke 的初始状态会传入子图（字段对齐时）。
- 子图 TypedDict 多出的键仅在子图内部可见，父图输出按 ParentState 过滤。
- 注意：本例用原地 append 修改共享列表以便观察，生产代码更推荐返回新列表的不可变风格。
“””

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class ParentState(TypedDict):
    parent_messages: list


class SubgraphState(TypedDict):
    parent_messages: list
    sub_message: str


def subgraph_node(state: SubgraphState) -> SubgraphState:
    state["parent_messages"].append("message from subgraph updateO(∩_∩)O")
    state["sub_message"] = "subgraph private message"
    return state


def parent_node(state: ParentState) -> ParentState:
    if not state.get("parent_messages"):
        state["parent_messages"] = []
    state["parent_messages"].append("message from 父亲 node")
    return state


def build_subgraph():
    sub_builder = StateGraph(SubgraphState)
    sub_builder.add_node("sub_node", subgraph_node)
    sub_builder.add_edge(START, "sub_node")
    sub_builder.add_edge("sub_node", END)
    return sub_builder.compile()


def build_parent_graph(compiled_subgraph):
    builder = StateGraph(ParentState)
    builder.add_node("parent_node", parent_node)
    builder.add_node("subgraph_node", compiled_subgraph)
    builder.add_edge(START, "parent_node")
    builder.add_edge("parent_node", "subgraph_node")
    builder.add_edge("subgraph_node", END)
    return builder.compile()


def main():
    compiled_subgraph = build_subgraph()
    parent_graph = build_parent_graph(compiled_subgraph)
    initial_state = {"parent_messages": ["我是父消息"]}
    print("初始状态：", initial_state)

    final_state = parent_graph.invoke(initial_state)
    print("\n执行后最终状态：", final_state)


if __name__ == "__main__":
    main()
"""
初始状态： {'parent_messages': ['我是父消息']}

执行后最终状态： {'parent_messages': ['我是父消息', 'message from 父亲 node', 'message from subgraph updateO(∩_∩)O']}
"""
