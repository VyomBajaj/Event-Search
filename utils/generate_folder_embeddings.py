from deepface import DeepFace
import json
import os

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



def generate_single_image_embedding(
    image_path,
    event_id,
    image_id
):

    data = load_data()


    if event_id not in data:

        data[event_id] = []



    try:

        embeddings = DeepFace.represent(

            img_path=str(image_path),

            model_name='ArcFace',

            enforce_detection=False,

            detector_backend='retinaface'
        )




        data[event_id].append({

            "image_id": image_id,

            "embedding": [
                e['embedding']
                for e in embeddings
            ]
        })



        save_data(data)

        print(
            f"Stored embedding for image:"
            f" {image_id}"
        )



    except Exception as e:

        print(
            f"Embedding generation failed:"
            f" {image_path}"
        )

        print(e)