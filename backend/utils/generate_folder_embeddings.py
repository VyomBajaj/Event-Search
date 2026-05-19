from deepface import DeepFace

def generate_single_image_embedding(
    image_path,
    image_id
):


    try:

        embeddings = DeepFace.represent(

            img_path=str(image_path),

            model_name='ArcFace',

            enforce_detection=False,

            detector_backend='retinaface'
        )


        embedding_vectors = [
                e['embedding']
                for e in embeddings
            ]

        print(
            f"Stored embedding for image:"
            f" {image_id}"
        )

        return embedding_vectors


    except Exception as e:

        print(
            f"Embedding generation failed:"
            f" {image_path}"
        )

        print(e)