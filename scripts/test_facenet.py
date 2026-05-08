from deepface import DeepFace

emb1 = DeepFace.represent("data/me1.jpg", model_name="ArcFace",detector_backend="retinaface")[0]["embedding"]
emb2 = DeepFace.represent("data/kavish.jpg", model_name="ArcFace",detector_backend="retinaface")[0]["embedding"]

print(len(emb1))  # should be 128 or 512

import numpy as np

def cosine_distance(a, b):
    a = np.array(a)
    b = np.array(b)
    return 1 - (np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

print("Distance:", cosine_distance(emb1, emb2))

print(emb1[:5])
print(emb2[:5])