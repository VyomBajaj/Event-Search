from pathlib import Path

# root of project
BASE_DIR = Path(__file__).resolve().parent.parent

# important paths
UPLOAD_DIR = BASE_DIR / "backend" / "uploads"
DATA_DIR = BASE_DIR / "data"
STORE_PATH = BASE_DIR / "scripts" / "store.json"