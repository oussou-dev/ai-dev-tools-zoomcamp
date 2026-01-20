from pathlib import Path

# Root directory
root = Path(__file__).parent

# Target directories
target_dirs = [
    "app",
    "app/agents",
    "app/database",
    "app/profiles",
    "app/scrapers",
    "app/services",
    "docker",
]

if __name__ == "__main__":
    for dir_name in target_dirs:
        dir_path = root / dir_name


        # Check if directory exists
        if not dir_path.exists():
            print(f"Directory does not exist: {dir_path}")
            continue

        init_file = dir_path / "__init__.py"

        # Check if __init__.py already exists
        if init_file.exists():
            print(f"Already exists in {dir_path}")
        else:
            # Create empty __init__.py
            init_file.touch()
            print(f"Created __init__.py in {dir_path}")
