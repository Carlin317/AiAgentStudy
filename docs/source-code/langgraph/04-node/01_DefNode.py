“””
【案例 04-1】节点定义方式与可选参数：普通节点、带额外参数的节点（partial 绑定）、以及 add_node 时配置 RetryPolicy

知识点速览：
- 节点返回值是对 State 的局部更新 dict；额外参数可用 functools.partial 预先绑定。
- add_node(name, func, retry_policy=RetryPolicy(...))：节点除了函数本身，还能挂执行策略。
“””

from functools import partial
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy
from requests import RequestException, Timeout


class GraphState(TypedDict):
    process_data: dict


# ========== 1. 定义节点函数 ==========
def input_node(state: GraphState) -> dict:
    print(f"input_node 收到: {state}")
    return {"process_data": {"input": "input_value"}}


def process_node(state: dict, param1: int, param2: str) -> dict:
    print(state, param1, param2)
    return {"process_data": {"process": "process_value"}}


# ========== 2. 定义重试策略 ==========
retry_policy = RetryPolicy(
    max_attempts=3,
    initial_interval=1,
    jitter=True,
    backoff_factor=2,
    retry_on=[RequestException, Timeout],
)

# ========== 3. 构建图 ==========
state_graph = StateGraph(GraphState)
state_graph.add_node("input", input_node)
# 用 partial 绑定额外参数后传给 add_node
process_with_params = partial(process_node, param1=100, param2="test")
state_graph.add_node("process", process_with_params, retry_policy=retry_policy)
state_graph.add_edge(START, "input")
state_graph.add_edge("input", "process")
state_graph.add_edge("process", END)

# ========== 4. 编译并执行 ==========
graph = state_graph.compile()

print(state_graph.edges)
print(state_graph.nodes)
print(graph.get_graph().print_ascii())
print()

initial_state = {"process_data": 5}
result = graph.invoke(initial_state)
print(f"最后的结果是: {result}")

"""
【输出示例】
{('process', '__end__'), ('__start__', 'input'), ('input', 'process')}
{'input': StateNodeSpec(runnable=input(tags=None, recurse=True, explode_args=False, func_accepts={}), metadata=None, input_schema=<class '__main__.GraphState'>, retry_policy=None, cache_policy=None, ends=(), defer=False), 'process': StateNodeSpec(runnable=process(tags=None, recurse=True, explode_args=False, func_accepts={}), metadata=None, input_schema=<class '__main__.GraphState'>, retry_policy=RetryPolicy(initial_interval=1, backoff_factor=2, max_interval=128.0, max_attempts=3, jitter=True, retry_on=[<class 'requests.exceptions.RequestException'>, <class 'requests.exceptions.Timeout'>]), cache_policy=None, ends=(), defer=False)}
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
 +---------+   
 | __end__ |   
 +---------+   
None

input_node 收到: {'process_data': 5}
{'process_data': {'input': 'input_value'}} 100 test
最后的结果是: {'process_data': {'process': 'process_value'}}
"""
