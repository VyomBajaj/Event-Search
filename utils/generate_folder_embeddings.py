from deepface import DeepFace
import json
import os
from pathlib import Path
from backend.config import BASE_DIR


def get_json_path():
    return BASE_DIR / "scripts" / "store.json"


def save_data(data):
    with open(get_json_path(), 'w') as f:
        json.dump(data, f, indent=2)


def load_data():
    json_path = get_json_path()
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return json.load(f)
    return {}


def check(folder_key, data):
    return folder_key in data


def generate_folder_embeddings(folder_path):

    if not folder_path.exists():
        raise Exception(f"Folder not found: {folder_path}")

    data = load_data()
    folder_key = folder_path.name

    if check(folder_key, data):
        print(f"Embeddings already exist for event: {folder_key}")
        return

    image_paths = [
        file for file in folder_path.glob("*")
        if file.suffix.lower() in [".jpg", ".png", ".jpeg", ".webp"]
    ]

    store = {}

    for file_path in image_paths:
        try:
            embeddings = DeepFace.represent(
                img_path=str(file_path),
                model_name='ArcFace',
                enforce_detection=False,
                detector_backend='retinaface'
            )

            relative_path = str(file_path.relative_to(folder_path.parent))
            store[relative_path] = [e['embedding'] for e in embeddings]

        except Exception as e:
            print(f"Skipping {file_path}: {e}")

    data[folder_key] = store
    save_data(data)

    print(f"Stored embeddings for event: {folder_key}")