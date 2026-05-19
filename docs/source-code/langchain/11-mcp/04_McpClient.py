"""
[案例 11-4]本地 MCP 天气客户端(直接调用服务端已注册工具)

知识点速览:
- MCP 客户端职责:连接服务端,发现能力,发起调用
- 本案例为同进程演示:通过 import 直接拿到服务端 mcp 实例,未走真实 MCP 协议通信
- 目的是先看懂"工具暴露 -> 能力发现 -> 发起调用"最小路径
- 生产环境中客户端通常通过 stdio 或 HTTP 连接独立的 MCP 服务
"""

import json
from loguru import logger

from McpServer import mcp


class MCPWeatherClient:
    """教学版客户端:直接访问服务端注册表."""

    def __init__(self, mcp_instance):
        self.mcp_instance = mcp_instance
        # 真实 MCP 客户端不会直接碰 _tools,而是通过协议发现能力
        self.available_tools = mcp_instance._tools

    def check_tool_availability(self, tool_name: str) -> bool:
        is_available = tool_name in self.available_tools
        if is_available:
            logger.info(f"工具 '{tool_name}' 可用")
        else:
            logger.warning(f"工具 '{tool_name}' 未在服务端注册")
        return is_available

    def call_get_weather(self, city: str) -> str or None:
        """调用服务端的 get_weather 工具"""
        tool_name = "get_weather"
        if not self.check_tool_availability(tool_name):
            return None

        try:
            weather_result = self.available_tools[tool_name](city)
            logger.info(
                f"成功获取 {city} 天气数据,返回结果长度:{len(weather_result)}"
            )
            return weather_result
        except Exception as exc:
            logger.error(f"调用 {tool_name} 工具失败:{str(exc)}")
            return None


def run_client_demo():
    """客户端演示:查询多城市天气并格式化输出"""
    logger.info("初始化 MCP 天气客户端...")
    client = MCPWeatherClient(mcp)

    target_cities = ["Beijing", "Shanghai"]
    for city in target_cities:
        logger.info(f"\n========== 查询 {city} 天气 ==========")
        weather_data = client.call_get_weather(city)
        if weather_data:
            formatted_data = json.dumps(
                json.loads(weather_data), indent=4, ensure_ascii=False
            )
            print(f"格式化天气结果:\n{formatted_data}")
        print("-" * 50)


if __name__ == "__main__":
    logger.info("启动 MCP 天气客户端...")
    run_client_demo()
