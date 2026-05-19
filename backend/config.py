from pathlib import Path
from dotenv import load_dotenv
import os
import cloudinary


BASE_DIR = Path(__file__).resolve().parent


load_dotenv(BASE_DIR / ".env")


UPLOAD_DIR = BASE_DIR / "uploads"

DATA_DIR = BASE_DIR

STORE_PATH = BASE_DIR / "scripts" / "store.json"


cloudinary.config(

    cloud_name=os.getenv(
        "CLOUDINARY_CLOUD_NAME"
    ),

    api_key=os.getenv(
        "CLOUDINARY_API_KEY"
    ),

    api_secret=os.getenv(
        "CLOUDINARY_API_SECRET"
    ),

    secure=True
)