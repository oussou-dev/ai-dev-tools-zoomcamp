Prompt_25
```
# Task_1
Generate a utility script named `init_packages.py` at the root of the project.

# Goal
This script ensures that every subdirectory inside the `app/` folder contains an `__init__.py` file, making them proper Python packages.

# Logic
1.  Import `pathlib`.
2.  Define the root directory as the current directory.
3.  Target specific directories: `app`, `app/agents`, `app/database`, `app/profiles`, `app/scrapers`, `app/services`, `docker`.
4.  For each directory:
    - Check if it exists.
    - Check if `__init__.py` exists inside it.
    - If not, create an empty `__init__.py` file.
    - Print a message: "Created __init__.py in {path}" or "Already exists in {path}".

# Execution
Add `if __name__ == "__main__":` to run the logic immediately.
```


