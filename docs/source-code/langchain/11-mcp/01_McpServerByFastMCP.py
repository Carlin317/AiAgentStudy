"""
[案例 11-1]使用 FastMCP 官方库搭建 MCP 服务端(工具 / 资源 / 提示词)

知识点速览:
- FastMCP 通过 @mcp.tool(),@mcp.resource(),@mcp.prompt() 暴露三类核心能力
- Tool 偏 model-controlled,Resource 偏 application-driven,Prompt 偏 user-controlled
- transport="stdio" 通过标准输入/输出通信,适合本地开发和 IDE 插件
- 直接在终端运行 stdio 服务会报 Invalid JSON,因为 stdio 服务应由宿主进程启动
"""

# pip install mcp
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo")


# ========== 1. 工具:可执行动作 ==========
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


# ========== 2. 资源:可读取内容 ==========
@mcp.resource("greeting://default")
def get_greeting() -> str:
    return "Hello from static resource!"


# ========== 3. 提示词模板 ==========
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
        "casual": "写一句轻松的问候",
    }
    return f"为{name}{styles.get(style, styles['friendly'])}"


if __name__ == "__main__":
    # STDIO 模式:由 Cursor/Claude 等 MCP 客户端启动本进程并接管 stdin/stdout
    # 直接运行会因终端输入被当作 JSON 解析而报错,属预期现象
    mcp.run(transport="stdio")


"""
常见问题:

1. ModuleNotFoundError: No module named 'pywintypes'
   → Windows 下需 pip install pywin32

2. 直接运行报 Invalid JSON / Internal Server Error
   → STDIO 模式需由 MCP 客户端启动,终端单独运行会解析失败,属正常现象
"""
