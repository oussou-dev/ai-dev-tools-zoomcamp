from pathlib import Path


def init_packages():
    """
    Ensure all app subdirectories have __init__.py files to make them proper Python packages.
    """
    # Define root directory
    root = Path.cwd()
    
    # Target directories to ensure they're Python packages
    target_dirs = [
        root / "app",
        root / "app" / "agents",
        root / "app" / "database",
        root / "app" / "profiles",
        root / "app" / "scrapers",
        root / "app" / "services",
        root / "docker",
    ]
    
    print("Initializing Python packages...")
    print("=" * 60)
    
    for directory in target_dirs:
        # Check if directory exists
        if not directory.exists():
            print(f"⚠ Directory does not exist: {directory.relative_to(root)}")
            continue
        
        # Check if __init__.py exists
        init_file = directory / "__init__.py"
        
        if init_file.exists():
            print(f"✓ Already exists in {directory.relative_to(root)}")
        else:
            # Create empty __init__.py
            init_file.touch()
            print(f"✓ Created __init__.py in {directory.relative_to(root)}")
    
    print("=" * 60)
    print("Package initialization complete!")


if __name__ == "__main__":
    init_packages()
