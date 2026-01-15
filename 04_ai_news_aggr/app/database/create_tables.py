import sys
from pathlib import Path

# Add project root to Python path for proper imports
# This file is at app/database/create_tables.py, so we need to go up 2 levels
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.database.models import Base
from app.database.connection import engine


if __name__ == "__main__":
    # Create all tables defined in the models
    Base.metadata.create_all(engine)
    print("Tables created successfully")
