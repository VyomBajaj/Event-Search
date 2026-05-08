from deepface import DeepFace
from pathlib import Path
def generate_query_embeddings(query_img_path, folder_path):
    query_path = Path(query_img_path)
    if not query_path.is_absolute():
        query_path = folder_path / query_path

    query_abs = str(query_path.resolve())
    query_embedding = DeepFace.represent(
        img_path=query_abs,
        model_name='ArcFace',
        enforce_detection=False,
        detector_backend='retinaface'
    )[0]['embedding']
    return query_abs,query_embedding