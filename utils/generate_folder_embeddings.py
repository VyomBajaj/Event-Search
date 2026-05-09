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


def check(event_id, data):
    return event_id in data


def generate_folder_embeddings(folder_path, event_id):

    if not folder_path.exists():
        raise Exception(f"Folder not found: {folder_path}")

    data = load_data()

    if check(event_id, data):
        print(f"Embeddings already exist for event: {event_id}")
        return

    image_paths = [
        file for file in folder_path.glob("*")
        if file.suffix.lower() in [".jpg", ".png", ".jpeg", ".webp"]
    ]

    store = []

    for file_path in image_paths:

        try:

            embeddings = DeepFace.represent(
                img_path=str(file_path),
                model_name='ArcFace',
                enforce_detection=False,
                detector_backend='retinaface'
            )

            store.append({
                "image_name": file_path.name,
                "embedding": [e['embedding'] for e in embeddings]
            })

        except Exception as e:
            print(f"Skipping {file_path}: {e}")

    data[event_id] = store

    save_data(data)

    print(f"Stored embeddings for event: {event_id}")