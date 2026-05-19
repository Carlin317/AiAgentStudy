"""
[案例 11-5]基于 mcp.json + LangChain Agent 的 MCP 客户端(LLM + MCP 工具)

知识点速览:
- 从 mcp.json 加载 MCP 服务配置,MultiServerMCPClient 连接多台 MCP 服务并获取工具列表
- 工具交给 create_tool_calling_agent + AgentExecutor,形成 LLM + MCP 工具的对话 Agent
- mcp.json 是客户端侧的连接配置约定,描述"有哪些服务,分别怎么连"
- 依赖:pip install langchain-mcp-adapters langchain-openai langchain-classic loguru
"""

import asyncio
import json
import os
from pathlib import Path

from loguru import logger

_MCP_JSON_PATH = Path(__file__).resolve().parent / "mcp.json"


def load_servers(file_path: str | Path | None = None) -> dict:
    """加载 MCP 服务器配置(客户端连接约定,非协议本体)."""
    path = Path(file_path) if file_path else _MCP_JSON_PATH
    if not path.exists():
        logger.warning(f"未找到 mcp 配置文件: {path}")
        return {"mcpServers": {}}
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    logger.info(
        f"已加载 mcp 配置: {path},共 {len(config.get('mcpServers', {}))} 个服务"
    )
    return config


async def run_chat_loop(config_path: str | Path | None = None) -> None:
    """启动基于 MCP 工具的聊天 Agent 循环."""
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
    except ImportError as e:
        logger.error(
            "请先安装 langchain-mcp-adapters: pip install langchain-mcp-adapters"
        )
        raise e

    from langchain_openai import ChatOpenAI
    from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

    config = load_servers(config_path)
    servers = config.get("mcpServers", {})
    if not servers:
        logger.warning("mcp.json 中未配置任何服务,无法获取 MCP 工具")
        return

    # ========== 1. 初始化 MCP 客户端并获取工具 ==========
    client = MultiServerMCPClient(connections=servers)
    tools = await client.get_tools()
    if not tools:
        logger.warning(
            "未从 MCP 服务获取到任何工具,请确认服务已启动且 mcp.json 配置正确"
        )
        return

    logger.info(f"已获取 {len(tools)} 个 MCP 工具: {[t.name for t in tools]}")

    # ========== 2. 语言模型 ==========
    llm = ChatOpenAI(
        model="deepseek-v4-flash",
        api_key=os.getenv("deepseek-api"),
        base_url="https://api.deepseek.com",
    )

    # ========== 3. 提示模板与 Agent ==========
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个有用的助手,需要使用提供的工具来完成用户请求."),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors="解析用户请求失败,请重新输入清晰的指令",
    )

    # ========== 4. 聊天循环 ==========
    logger.info("\n MCP Agent 已启动,输入提问给 (LLM+MCP),输入 'quit' 退出")

    while True:
        try:
            user_input = input("\n您: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "quit":
                logger.info("已退出")
                break
            result = agent_executor.invoke({"input": user_input})
            output = result.get("output", result)
            print(f"\nAgent: {output}")
        except KeyboardInterrupt:
            logger.info("已退出")
            break


def main() -> None:
    asyncio.run(run_chat_loop())


if __name__ == "__main__":
    main()
