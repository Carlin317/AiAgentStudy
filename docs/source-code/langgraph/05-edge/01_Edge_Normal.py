"""
[案例 05-1]普通边(Normal Edges):用 add_edge 串联节点,固定执行顺序,无条件跳转

知识点速览:
- add_edge(源节点, 目标节点):执行完源节点后必定进入目标节点,无分支.
- START,END 为内置虚拟节点,分别表示图入口与出口.
"""

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# ========== 1. 定义状态与节点 ==========
class DiliState(TypedDict):
    value: int
    step: str


def node_a(state: DiliState) -> dict:
    print("执行节点A")
    return {"value": state["value"] + 1, "step": "A执行完毕"}


def node_b(state: DiliState) -> dict:
    print("执行节点B")
    return {"value": state["value"] * 2, "step": "B执行完毕"}


def node_c(state: DiliState) -> dict:
    print("执行节点C")
    return {"value": state["value"] - 1, "step": "C执行完毕"}


# ========== 2. 构建并执行 ==========
def main():
    print("=== 普通边演示 ===")

    builder = StateGraph(DiliState)
    builder.add_node("node_a", node_a)
    builder.add_node("node_b", node_b)
    builder.add_node("node_c", node_c)

    builder.add_edge(START, "node_a")
    builder.add_edge("node_a", "node_b")
    builder.add_edge("node_b", "node_c")
    builder.add_edge("node_c", END)

    app = builder.compile()

    result = app.invoke({"value": 1})
    print(f"执行结果: {result}\n")
    print(builder.edges)
    print(app.get_graph().print_ascii())
    print("=================================")
    print()
    print(app.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()

"""
[输出示例]
=== 普通边演示 ===
执行节点A
执行节点B
执行节点C
执行结果: {'value': 3, 'step': 'C执行完毕'}

{('node_b', 'node_c'), ('__start__', 'node_a'), ('node_a', 'node_b'), ('node_c', '__end__')}
+-----------+  
| __start__ |  
+-----------+  
      *        
      *        
      *        
  +--------+   
  | node_a |   
  +--------+   
      *        
      *        
      *        
  +--------+   
  | node_b |   
  +--------+   
      *        
      *        
      *        
  +--------+   
  | node_c |   
  +--------+   
      *        
      *        
      *        
 +---------+   
 | __end__ |   
 +---------+   
None
=================================

---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        node_a(node_a)
        node_b(node_b)
        node_c(node_c)
        __end__([<p>__end__</p>]):::last
        __start__ --> node_a;
        node_a --> node_b;
        node_b --> node_c;
        node_c --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc

"""
