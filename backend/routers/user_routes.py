from fastapi import APIRouter, UploadFile, File, Form , HTTPException
from fastapi.responses import FileResponse
from config import UPLOAD_DIR, DATA_DIR , BASE_DIR
from utils.generate_query_embeddings import generate_query_embeddings
from utils.match_faces import match_faces
from services.cloudinary_service import upload_user_image
from utils.download_temp_image import download_temp_image
import os
from fastapi import HTTPException
from fastapi.responses import FileResponse
from services.mongo_service import get_image_by_id
from services.mongo_service import get_event_by_name

router = APIRouter(prefix="/user")

@router.post("/upload")
def upload_details(
    file: UploadFile = File(...),
    event: str = Form(...)
):

    try:

        # 1. Validate event name

        if not event.strip():

            return {
                "error": "Event name is required"
            }

        # 2. Validate file

        if not file:

            return {
                "error": "Image file is required"
            }

        # 3. Find event in MongoDB

        event_doc = get_event_by_name(
            event.strip()
        )

        if not event_doc:

            return {
                "error":
                "Event not found"
            }

        event_id = str(
            event_doc["_id"]
        )

        uploaded = upload_user_image(
            file,
            event_id
        )

        # 5. Cloudinary validation

        if not uploaded:

            return {
                "error":
                "Cloudinary upload failed"
            }

        if "error" in uploaded:

            return {
                "error":
                uploaded["error"]
            }

        # 6. Validate upload response

        if (
            "url" not in uploaded
            or "public_id" not in uploaded
        ):

            return {
                "error":
                "Invalid Cloudinary response"
            }
        
        # 7. Success response
        return {

            "message":
            "Upload successful",

            "event_id":
            event_id,

            "image_url":
            uploaded["url"],

            "public_id":
            uploaded["public_id"]
        }

    except Exception as e:

        print("UPLOAD ERROR:")
        print(e)

        return {
            "error": str(e)
        }


@router.post("/getPhotos")
def get_photos(
    event_id: str = Form(...),
    image_url: str = Form(...)
):


    # 1. Download query image temp

    query_path = download_temp_image(
        image_url
    )

    try:

        # 2. Generate query embedding

        _, query_embedding = (
            generate_query_embeddings(
                query_path,
                query_path.parent
            )
        )

        # 3. Match faces

        results = match_faces(
            event_id,
            query_embedding,
            threshold=0.45
        )

        # 4. Fetch MongoDB metadata

        clean_results = []

        for item in results:

            image_id = item["image_id"]

            score = item["score"]

            image_doc = (
                get_image_by_id(
                    image_id,
                )
            )

            if not image_doc:
                continue

            clean_results.append({
                "image": image_doc["image_url"],
                "score": round(score, 4)
            })

        return {
            "message": "Matches found",
            "count": len(clean_results),
            "results": clean_results
        }

    except Exception as e:

        print("GET PHOTOS ERROR:")
        print(e)

        return {
            "error": str(e)
        }

    finally:

        if os.path.exists(query_path):
            
            os.remove(query_path)



@router.get("/download")
def download_file(path: str):

    # join safely with DATA_DIR
    file_path = (DATA_DIR / path).resolve()
    # print("PATH RECEIVED:", path)
    # print("DATA_DIR:", DATA_DIR)
    # print("FULL PATH:", file_path)
    # print("EXISTS:", file_path.exists())

    # security check
    if not str(file_path).startswith(str(DATA_DIR.resolve())):
        raise HTTPException(status_code=403, detail="Forbidden")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Not found")
    
    

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/octet-stream"
    )