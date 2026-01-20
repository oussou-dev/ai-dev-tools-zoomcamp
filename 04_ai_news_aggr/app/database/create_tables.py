import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.database.models import Base
from app.database.connection import engine


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables created successfully")
