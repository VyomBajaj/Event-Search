import os
import json
import numpy as np

from backend.config import STORE_PATH


def get_json_path():

    return STORE_PATH


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def load_data():

    json_path = get_json_path()

    if (
        os.path.exists(json_path)
        and os.path.getsize(json_path) > 0
    ):

        with open(json_path, 'r') as f:
            return json.load(f)

    return {}

EMBEDDINGS_CACHE = load_data()
def match_faces(event_id, query_embedding,
                k=10, threshold=0.45):

    data = EMBEDDINGS_CACHE

    if event_id not in data:
        print("No embeddings found for event")
        return []

    event_embeddings = data[event_id]

    scores = []

    query_embedding = np.array(query_embedding)

    for item in event_embeddings:

        image_id = item["image_id"]

        embed_list = item["embedding"]

        if not embed_list:
            continue

        if isinstance(embed_list[0], list):

            max_sim = max(
                cosine_similarity(
                    query_embedding,
                    np.array(face_embed)
                )
                for face_embed in embed_list
            )

        else:

            max_sim = cosine_similarity(
                query_embedding,
                np.array(embed_list)
            )

        if max_sim >= threshold:

            scores.append({
                "image_id": image_id,
                "score": float(max_sim)
            })

    scores.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scores