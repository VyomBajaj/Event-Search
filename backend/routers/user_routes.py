from fastapi import APIRouter, UploadFile, File, Form , HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from backend.config import UPLOAD_DIR
import shutil
from backend.config import UPLOAD_DIR, DATA_DIR , BASE_DIR
from utils.generate_query_embeddings import generate_query_embeddings
from utils.match_faces import match_faces
from backend.services.cloudinary_service import upload_user_image
from utils.download_temp_image import download_temp_image
import os
from fastapi import HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from backend.config import DATA_DIR

router = APIRouter(prefix="/user")

@router.post("/upload")
async def upload_details(
    file: UploadFile = File(...),
    event: str = Form(...)
):
    # # 1. Create event folder
    # event_path = UPLOAD_DIR / event
    # event_path.mkdir(parents=True, exist_ok=True)

    # # 2. Save file
    # file_path = event_path / file.filename

    # with open(file_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)

    # 3. Return response (DO NOT return full system path)
    uploaded = upload_user_image(file, event)

    if "error" in uploaded:
        return {
            "message": "Cloudinary upload failed",
            "error": uploaded["error"]
        }

    return {
        "message": "Upload successful",
        "event": event,
        "image_url": uploaded["url"],
        "public_id": uploaded["public_id"]
    }


@router.post("/getPhotos")
async def get_photos(
    event: str = Form(...),
    image_url: str = Form(...)
):

    # 1. Download cloud image temporarily
    query_path = download_temp_image(image_url)

    try:

        # 2. Dataset path
        folder_path = DATA_DIR / event

        if not folder_path.exists():
            return {"error": "Event data not found"}

        # 3. Generate query embedding
        query_abs, query_embedding = generate_query_embeddings(
            query_path,
            folder_path
        )

        # 4. Match faces
        results = match_faces(
            folder_path,
            query_abs,
            query_embedding,
            k=10
        )

        # 5. Clean frontend response
        clean_results = [
            {
                "image": f"http://127.0.0.1:8000/static/{Path(path).relative_to(BASE_DIR / 'data')}",
                "score": round(float(score), 4)
            }
            for path, score in results
        ]

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

        # 6. Cleanup temp image
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