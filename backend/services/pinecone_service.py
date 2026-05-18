from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index(
    os.getenv("PINECONE_INDEX_NAME")
)

def test_pinecone():

    print(index.describe_index_stats())


def store_embedding(
    image_id,
    event_id,
    embedding
):

    index.upsert(
        vectors=[
            {
                "id": image_id,

                "values": embedding,

                "metadata": {
                    "event_id": event_id
                }
            }
        ]
    )

def search_similar_faces(
    query_embedding,
    event_id,
    top_k=100
):

    results = index.query(

        vector=query_embedding,

        top_k=top_k,

        filter={
            "event_id": event_id
        },

        include_metadata=True
    )
    # print(results)
    return results