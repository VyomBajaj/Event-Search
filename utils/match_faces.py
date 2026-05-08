from pathlib import Path
from deepface import DeepFace
import os
import json
import numpy as np
from backend.config import STORE_PATH

def get_json_path():
    
    return STORE_PATH

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def load_data():
    json_path = get_json_path()
    
    if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
        with open(json_path, 'r') as f:
            return json.load(f)
    
    return {}


def match_faces(folder_path, query_abs, query_embedding, k=10, threshold=0.45):

    data = load_data()
    folder_key = folder_path.name

    if folder_key not in data:
        print("No embeddings found for this folder")
        return []

    folder_embeddings = data[folder_key]
    scores = []

    query_embedding = np.array(query_embedding)

    for rel_path, embed_list in folder_embeddings.items():

        if not embed_list:
            continue

        full_path = str((folder_path.parent / rel_path).resolve())

        if full_path == query_abs:
            continue

        if isinstance(embed_list[0], list):
            max_sim = max(
                cosine_similarity(query_embedding, np.array(face_embed))
                for face_embed in embed_list
            )
        else:
            max_sim = cosine_similarity(query_embedding, np.array(embed_list))

        if max_sim >= threshold:
            scores.append((full_path, max_sim))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores