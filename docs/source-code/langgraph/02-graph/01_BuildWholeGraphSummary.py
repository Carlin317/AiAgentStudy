"""
[案例 02-1]多节点,固定边的完整图:input → process → output 三个节点,演示图的完整搭建流程

知识点速览:
- StateGraph(GraphState) 指定状态类型后,各节点接收完整 state,返回"部分更新"字典.
- 未为字段指定 Reducer 时默认覆盖:后一节点返回的 process_data 会覆盖前一节点的值.
- 固定边:add_edge 依次串联 START → input → process → output → END,执行顺序确定.
"""

from typing import TypedDict
from langgraph.constants import START, END
from langgraph.graph import StateGraph

# ========== 1. 定义状态 ==========
class GraphState(TypedDict):
    process_data: dict


# ========== 2. 定义节点函数 ==========
def input_node(state: GraphState) -> dict:
    print(f"input_node 节点执行 state.get('process_data'): {state.get('process_data')}")
    return {"process_data": {"input": "input_value"}}


def process_node(state: dict) -> dict:
    print(
        f"process_node 节点执行 state.get('process_data'): {state.get('process_data')}"
    )
    return {"process_data": {"process": "process_value9527"}}


def output_node(state: GraphState) -> dict:
    print(
        f"output_node 节点执行 state.get('process_data'): {state.get('process_data')}"
    )
    return {"process_data": state.get("process_data")}


# ========== 3. 构建图 ==========
graph = StateGraph(GraphState)
graph.add_node("input", input_node)
graph.add_node("process", process_node)
graph.add_node("output", output_node)

# 固定边
graph.add_edge(START, "input")
graph.add_edge("input", "process")
graph.add_edge("process", "output")
graph.add_edge("output", END)

# ========== 4. 编译并执行 ==========
app = graph.compile()
result = app.invoke({"process_data": {"name": "测试数据", "value": 123456}})
print(f"最后的结果是:{result}")

# ========== 5. 可视化 ==========
print(app.get_graph().print_ascii())
print("=================================")
print(app.get_graph().draw_mermaid())


"""
[输出示例]
input_node 节点执行 state.get('process_data'): {'name': '测试数据', 'value': 123456}
process_node 节点执行 state.get('process_data'): {'input': 'input_value'}
output_node 节点执行 state.get('process_data'): {'process': 'process_value9527'}
最后的结果是:{'process_data': {'process': 'process_value9527'}}
+-----------+
| __start__ |
+-----------+
      *
      *
      *
  +-------+
  | input |
  +-------+
      *
      *
      *
 +---------+
 | process |
 +---------+
      *
      *
      *
  +--------+
  | output |
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
        input(input)
        process(process)
        output(output)
        __end__([<p>__end__</p>]):::last
        __start__ --> input;
        input --> process;
        process --> output;
        output --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""
