import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pathlib import Path
import numpy as np
from utils.generate_folder_embeddings import generate_folder_embeddings
from utils.generate_query_embeddings import generate_query_embeddings
from utils.match_faces import match_faces
from backend.config import BASE_DIR

folder_path = BASE_DIR/"data"/"wedding1"

generate_folder_embeddings(folder_path)
query_abs,query_embedding = generate_query_embeddings("me2.jpg",folder_path)
results = match_faces(folder_path,query_abs,query_embedding, k=6)

print("\nTop Matches:")
for path, score in results:
    print(path, round(score, 4))