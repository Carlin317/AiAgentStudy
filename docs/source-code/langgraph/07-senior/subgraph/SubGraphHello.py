“””
【案例 07-9】子图作为节点：将 compile 后的子图直接 add_node 进父图；
父子共用同一 State 类型时，由 Reducer 合并 messages。

对应教程章节：第 25 章 - LangGraph 高级特性 → 4、子图（Subgraphs）

知识点速览：
- 编译后的图可以像节点一样被父图注册。
- 父子状态结构相同且 messages 使用 add 时，会出现重复前缀——用来观察父图和子图各自合并一次的效果。
“””

from operator import add
from typing import Annotated, TypedDict

from langgraph.constants import END
from langgraph.graph import StateGraph, START


class DiliState(TypedDict):
    messages: Annotated[list[str], add]


def sub_node(state: DiliState) -> DiliState:
    return {"messages": ["response from subgraph"]}


# ========== 1. 子图 ==========
subgraph_builder = StateGraph(DiliState)
subgraph_builder.add_node("sub_node", sub_node)
subgraph_builder.add_edge(START, "sub_node")
subgraph_builder.add_edge("sub_node", END)
subgraph = subgraph_builder.compile()

# ========== 2. 父图 ==========
builder = StateGraph(DiliState)
builder.add_node("subgraph_node", subgraph)
builder.add_edge(START, "subgraph_node")
builder.add_edge("subgraph_node", END)

graph = builder.compile()

# ========== 3. 执行与观察 ==========
# 状态传递：主图 → 子图(add 合并) → 主图(再次 add 合并)，因此 "main-graph" 出现两次
print(graph.invoke({"messages": ["main-graph"]}))
print()

print(subgraph.get_graph().draw_mermaid())
print("=" * 50)
print()

"""
【输出示例】
{'messages': ['main-graph', 'main-graph', 'response from subgraph']}

---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        sub_node(sub_node)
        __end__([<p>__end__</p>]):::last
        __start__ --> sub_node;
        sub_node --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc

==================================================
"""
