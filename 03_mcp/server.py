from fastmcp import FastMCP
import requests
import os
import zipfile
from minsearch import Index

mcp = FastMCP("Demo 🚀")

# Minsearch index (global, initialized lazily)
_docs_index = None
ZIP_URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
ZIP_PATH = "fastmcp-main.zip"

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

def download_fastmcp_docs() -> str:
    """Download fastmcp zip if not already present."""
    if os.path.exists(ZIP_PATH):
        return f"Already downloaded: {ZIP_PATH}"
    response = requests.get(ZIP_URL)
    response.raise_for_status()
    with open(ZIP_PATH, "wb") as f:
        f.write(response.content)
    return f"Downloaded: {ZIP_PATH}"

def index_docs() -> Index:
    """Extract md/mdx files from zip and index with minsearch."""
    global _docs_index
    if _docs_index is not None:
        return _docs_index
    
    download_fastmcp_docs()
    
    docs = []
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        for name in zf.namelist():
            if name.endswith(".md") or name.endswith(".mdx"):
                # Remove first path component (e.g., "fastmcp-main/")
                parts = name.split("/", 1)
                filename = parts[1] if len(parts) > 1 else parts[0]
                content = zf.read(name).decode("utf-8", errors="ignore")
                docs.append({"filename": filename, "content": content})
    
    _docs_index = Index(text_fields=["content"], keyword_fields=["filename"])
    _docs_index.fit(docs)
    return _docs_index

@mcp.tool
def search_docs(query: str) -> list[dict]:
    """Search fastmcp documentation and return 5 most relevant results."""
    return _search_docs(query)

def _search_docs(query: str) -> list[dict]:
    index = index_docs()
    results = index.search(query, num_results=5)
    return results

if __name__ == "__main__":
    mcp.run()