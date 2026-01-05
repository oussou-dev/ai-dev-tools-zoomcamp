# MCP Homework - Module 03

This project implements an MCP (Model Context Protocol) server with tools for web scraping and documentation search.

[MCP Homework](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2025/03-mcp/homework.md)

## Setup

```bash
pip install uv
uv init
uv add fastmcp
```

## Homework Answers

<details>
<summary>Question 1: First Hash in FastMCP Wheels Section</summary>

```
sha256:e33cd622e1ebd5110af6a981804525b6cd41072e3c7d68268ed69ef3be651aca
```
</details>

<details>
<summary>Question 2: FastMCP Transport</summary>

**Answer: STDIO**
</details>

<details>
<summary>Question 3: Scrape Web Tool - Character Count</summary>

Retrieved content from `https://github.com/alexeygrigorev/minsearch`: approximately **29184** characters (actual: ~31361).
</details>

<details>
<summary>Question 4: Word Count for "data" on datatalks.club</summary>

**Answer: 61**
</details>

<details>
<summary>Question 5: First File for "demo" Query</summary>

**Answer: examples/testing_demo/README.md**
</details>

<details>
<summary>Question 6: Search Tool</summary>

Implemented `search_docs` tool in `server.py`.
</details>

## Tools Implemented

1. **`add(a, b)`** - Add two numbers
2. **`fetch_web_content(url)`** - Fetch web content using Jina Reader
3. **`search_docs(query)`** - Search fastmcp documentation (returns 5 most relevant docs)

## Running the Server

```bash
uv run server.py
```

## Testing

```bash
uv run search.py
```
