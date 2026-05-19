"""
[案例 01-2]不接入大模型的业务图:用加法/减法节点演示同一个状态字段 x 沿节点逐步更新

知识点速览:
- 用 dict 作为 State 类型时无需预定义 TypedDict,适合快速试验;字段增多后建议改为 TypedDict 或 Pydantic.
- 节点函数接收 state,返回要更新的键值对;未指定 Reducer 时默认覆盖旧值.
- graph.edges / graph.nodes 可在 compile() 前查看已注册的边与节点,适合排查连接问题.
"""

from langgraph.constants import START, END
from langgraph.graph import StateGraph


def addition(state):
    print(f"加法节点收到: {state}")
    return {"x": state["x"] + 1}


def subtraction(state):
    print(f"减法节点收到: {state}")
    return {"x": state["x"] - 2}


# ========== 1. 构建图 ==========
# 使用 dict 作为状态类型,无需预定义 TypedDict
graph = StateGraph(dict)
graph.add_node("addition", addition)
graph.add_node("subtraction", subtraction)

graph.add_edge(START, "addition")
graph.add_edge("addition", "subtraction")
graph.add_edge("subtraction", END)

# ========== 2. 调试:查看边与节点 ==========
print(graph.edges)
print(graph.nodes)

# ========== 3. 编译并执行 ==========
app = graph.compile()
initial_state = {"x": 5}
result = app.invoke(initial_state)
print(f"最后的结果是: {result}")

# ========== 4. 可视化 ==========
print(app.get_graph().print_ascii())
print()
print(app.get_graph().draw_mermaid())

"""
[输出示例]
{('subtraction', '__end__'), ('addition', 'subtraction'), ('__start__', 'addition')}
{'addition': StateNodeSpec(runnable=addition(tags=None, recurse=True, explode_args=False, func_accepts={}), metadata=None, input_schema=<class 'dict'>, retry_policy=None, cache_policy=None, ends=(), defer=False), 'subtraction': StateNodeSpec(runnable=subtraction(tags=None, recurse=True, explode_args=False, func_accepts={}), metadata=None, input_schema=<class 'dict'>, retry_policy=None, cache_policy=None, ends=(), defer=False)}
加法节点收到: {'x': 5}
减法节点收到: {'x': 6}
最后的结果是: {'x': 4}
 +-----------+
 | __start__ |
 +-----------+
        *
        *
        *
  +----------+
  | addition |
  +----------+
        *
        *
        *
+-------------+
| subtraction |
+-------------+
        *
        *
        *
  +---------+
  | __end__ |
  +---------+
None

---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        addition(addition)
        subtraction(subtraction)
        __end__([<p>__end__</p>]):::last
        __start__ --> addition;
        addition --> subtraction;
        subtraction --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""
