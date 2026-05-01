import sys
from pathlib import Path


# Allow tests/ to import backend modules like `from main import app`.
BACKEND_DIR = Path(__file__).resolve().parents[1] / "Backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
