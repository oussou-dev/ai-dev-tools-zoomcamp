from server import _search_docs

print("Testing search_docs...")
print("=" * 50)

query = "demo" #"how to create a tool"
print(f"Query: '{query}'")
print()

results = _search_docs(query)
print(f"Found {len(results)} results:")
print()

for i, result in enumerate(results, 1):
    print(f"--- Result {i} ---")
    print(f"Filename: {result['filename']}")
    preview = result['content'][:200].replace('\n', ' ')
    print(f"Preview: {preview}...")
    print()
