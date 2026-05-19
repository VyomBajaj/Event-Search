import os
import json
import numpy as np
from services.pinecone_service import (
    search_similar_faces
)

def match_faces(
    event_id,
    query_embedding,
    threshold=0.45
):

    results = search_similar_faces(

        query_embedding=query_embedding,

        event_id=event_id,

        top_k=100
    )



    matches = []



    for item in results["matches"]:

        score = float(item["score"])



        if score >= threshold:

            matches.append({

                "image_id": item["id"],

                "score": score
            })



    return matches