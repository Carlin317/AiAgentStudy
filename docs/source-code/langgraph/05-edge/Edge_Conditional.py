“””
【案例 05-3】条件边（Conditional Edges）：根据状态在多个后继节点中选一个执行

知识点速览：
- add_conditional_edges(source, route_fn, mapping)：route_fn(state) 返回值作为 key，在 mapping 中查到下一节点名。
- 条件边让边负责分流，而非把 if/else 塞回节点里；路由函数在 source 节点执行后被调用。
- State 也可以用 Pydantic BaseModel 定义，支持默认值和校验。
“””

from typing import Optional
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from loguru import logger
from pydantic import BaseModel


# ========== 1. 定义状态与节点 ==========
class MyState(BaseModel):
    x: int
    result: Optional[str] = None


def check_x(state: MyState) -> MyState:
    logger.info(f"[check_x] Received state: {state}")
    return state


def is_even(state: MyState) -> bool:
    """路由函数：返回 True/False 供条件边分流。"""
    return state.x % 2 == 0


def handle_even(state: MyState) -> MyState:
    logger.info("[handle_even] x 是偶数")
    return MyState(x=state.x, result="even")


def handle_odd(state: MyState) -> MyState:
    logger.info("[handle_odd] x 是奇数")
    return MyState(x=state.x, result="odd")


# ========== 2. 构建图 ==========
builder = StateGraph(MyState)
builder.add_node("check_x", check_x)
builder.add_node("handle_even", handle_even)
builder.add_node("handle_odd", handle_odd)


builder.add_conditional_edges(
    "check_x", is_even, {True: "handle_even", False: "handle_odd"}
)

builder.add_edge(START, "check_x")
builder.add_edge("handle_even", END)
builder.add_edge("handle_odd", END)

# ========== 3. 编译并执行 ==========
graph = builder.compile()
print(graph.get_graph().print_ascii())

logger.info("输入 x=4（偶数）")
graph.invoke(MyState(x=4))

# 测试奇数
# logger.info("输入 x=3（奇数）")
# graph.invoke(MyState(x=3))

"""
【输出示例】
              +-----------+               
              | __start__ |               
              +-----------+               
                    *                     
                    *                     
                    *                     
               +---------+                
               | check_x |                
               +---------+                
             ...          ..              
            .               ..            
          ..                  ..          
+-------------+           +------------+  
| handle_even |           | handle_odd |  
+-------------+           +------------+  
             ***          **              
                *       **                
                 **   **                  
               +---------+                
               | __end__ |                
               +---------+                
None
2026-03-23 16:38:23.954 | INFO     | __main__:<module>:108 - 输入 x=4（偶数）
2026-03-23 16:38:23.955 | INFO     | __main__:check_x:40 - [check_x] Received state: x=4 result=None
2026-03-23 16:38:23.955 | INFO     | __main__:handle_even:65 - [handle_even] x 是偶数
"""
