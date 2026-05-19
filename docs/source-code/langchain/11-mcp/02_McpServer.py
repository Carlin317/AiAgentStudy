"""
[案例 11-2]本地 MCP 天气服务端(极简实现,无 FastMCP 依赖)

知识点速览:
- 教学版极简 MCP 服务端:演示 @mcp.tool() 背后的注册思想
- 只模拟了"工具注册表 + 服务进程存活",未实现 JSON-RPC,握手等完整 MCP 通信
- 与 Tool 的区别:Tool 是单进程能力封装,MCP 在 Tool 之上加标准协议层,便于跨应用复用
- 仓库保留 transport="sse" 写法用于教学;初学者应先理解 stdio 和 HTTP/Streamable HTTP
"""

import json
import os
import httpx
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


# ========== 1. 极简 MCP 服务类(教学用,非生产级) ==========
class MCPWeatherServer:
    """只保留"注册工具"和"维持进程"两层概念."""

    def __init__(self, name: str, host: str, port: int):
        self.name = name
        self.host = host
        self.port = port
        self._tools = {}

    def tool(self):
        """@mcp.tool() 装饰器:把函数登记到工具注册表."""

        def decorator(func):
            self._tools[func.__name__] = func
            return func

        return decorator

    def run(self, transport: str):
        """模拟 run() 入口,只打印监听信息并保持进程存活."""
        if transport != "sse":
            logger.warning(f"不支持的传输协议 {transport},默认使用 SSE")
        logger.info(f"启动 MCP SSE 天气服务器,监听 http://{self.host}:{self.port}/sse")
        self._keep_alive()

    def _keep_alive(self):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logger.info("MCP 天气服务器已停止")


# ========== 2. 创建实例并注册工具 ==========
# 若改用 FastMCP:构造函数只接受服务名,host/port 在 run() 时传
# 参见 McpServerWeatherByFastMCP.py
mcp = MCPWeatherServer("WeatherServerSSE", host="127.0.0.1", port=8000)


@mcp.tool()
def get_weather(city: str) -> str:
    """
    查询指定城市的即时天气信息.
    参数 city: 城市英文名,如 Beijing
    返回: OpenWeather API 的 JSON 字符串
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric",
        "lang": "zh_cn",
    }
    resp = httpx.get(url, params=params, timeout=10)
    data = resp.json()
    logger.info(f"查询 {city} 天气结果:{data}")
    return json.dumps(data, ensure_ascii=False)


if __name__ == "__main__":
    logger.info("启动 MCP SSE 天气服务器,监听 http://127.0.0.1:8000/sse")
    mcp.run(transport="sse")
