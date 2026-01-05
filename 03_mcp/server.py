from fastmcp import FastMCP
import requests

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def fetch_web_content(url: str) -> str:
    """Fetch web content using Jina Reader"""
    return _fetch_web_content(url)

def _fetch_web_content(url: str) -> str:
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    return response.text

if __name__ == "__main__":
    mcp.run()