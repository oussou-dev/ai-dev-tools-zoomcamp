from server import _fetch_web_content

def count_characters(content: str) -> int:
    """Count and return the number of characters in the content."""
    return len(content)

print("Testing fetch_web_content...")
try:
    content = _fetch_web_content("https://github.com/alexeygrigorev/minsearch")
    char_count = count_characters(content)
    print(f"Character count: {char_count}")
    print("Content preview:")
    print(content[:200])
    print("\nSuccess!")
except Exception as e:
    print(f"Error: {e}")
