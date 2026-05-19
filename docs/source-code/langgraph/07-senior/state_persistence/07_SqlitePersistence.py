"""
[案例 07-7]SQLite 检查点 SqliteSaver:把检查点写入本地 .db 文件,进程重启仍可恢复同 thread_id 的会话.

对应教程章节:第 25 章 - LangGraph 高级特性 → 2,状态持久化(Persistence)

知识点速览:
- 依赖:langgraph-checkpoint-sqlite(生产环境更常用 langgraph-checkpoint-postgres).
- 与 InMemorySaver 用法相同,区别仅在存储介质:compile(checkpointer=...) / invoke / get_state.
- 重点是理解后端可替换,API 保持一致.
"""

import sqlite3
import operator
from pathlib import Path
from typing import Annotated, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END


class MyState(TypedDict):
    messages: Annotated[list, operator.add]


def node_1(state: MyState):
    return {"messages": ["abc", "def"]}


def main():
    db_dir = Path(__file__).resolve().parent / "sqlite_checkpoints"
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / "sqlite_data.db"

    conn = sqlite3.connect(database=str(db_path), check_same_thread=False)
    sqlite_db = SqliteSaver(conn=conn)

    builder = StateGraph(MyState)
    builder.add_node("node_1", node_1)
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", END)

    graph = builder.compile(checkpointer=sqlite_db)

    config = {"configurable": {"thread_id": "user-001"}}

    initial_state = graph.get_state(config)
    print(f"Initial state: {initial_state}")

    result = graph.invoke({"messages": []}, config)
    print(f"Result: {result}")

    print()
    print("========== 查看执行后的状态 ==========")
    final_state = graph.get_state(config)
    print()
    print(f"Final state: {final_state}")

    conn.close()


if __name__ == "__main__":
    main()

"""
[输出示例]
Initial state: StateSnapshot(values={}, next=(), config={'configurable': {'thread_id': 'user-001'}}, metadata=None, created_at=None, parent_config=None, tasks=(), interrupts=())
Result: {'messages': ['abc', 'def']}

========== 查看执行后的状态 ==========

Final state: StateSnapshot(values={'messages': ['abc', 'def']}, next=(), config={'configurable': {'thread_id': 'user-001', 'checkpoint_ns': '', 'checkpoint_id': '1f1272f0-d724-675e-8001-bb885d01bb16'}}, metadata={'source': 'loop', 'step': 1, 'parents': {}}, created_at='2026-03-24T03:10:46.773535+00:00', parent_config={'configurable': {'thread_id': 'user-001', 'checkpoint_ns': '', 'checkpoint_id': '1f1272f0-d723-6a48-8000-d3aac2954c9d'}}, tasks=(), interrupts=())
"""
