from fastapi import Form, APIRouter,UploadFile,File
from pathlib import Path
import tempfile
import shutil
import zipfile
from utils.generate_folder_embeddings import generate_single_image_embedding
from services.mongo_service import create_event_db
router = APIRouter(prefix='/admin')
from services.cloudinary_service import upload_dataset_image
from services.mongo_service import insert_image_db
from schemas.image_schema import ImageSchema
from services.pinecone_service import store_embedding


@router.post('/create-event')
async def create_event(event: str = Form(...)):

    event_id = create_event_db(event)

    if not event_id:
        return {
            "message": "Event already exists"
        }

    return {
        "message": "Event created successfully",
        "event_id": event_id
    }

@router.post('/upload-folder')
def upload_folder(
    event_id: str = Form(...),
    zip_file: UploadFile = File(...)
):

    temp_zip_path = None
    temp_extract_path = None
    processed_path = None

    try:
        # 1. Save ZIP temporarily
        temp_zip_path = (
            Path(tempfile.gettempdir())
            / zip_file.filename
        )

        with open(temp_zip_path, "wb") as buffer:

            shutil.copyfileobj(
                zip_file.file,
                buffer
            )
        
        # 2. Extract ZIP temporarily
        temp_extract_path = Path(
            tempfile.mkdtemp()
        )

        with zipfile.ZipFile(
            temp_zip_path,
            'r'
        ) as zip_ref:

            zip_ref.extractall(
                temp_extract_path
            )

        # 3. Flatten images

        processed_path = Path(
            tempfile.mkdtemp()
        )

        for file in temp_extract_path.rglob("*"):

            if file.name.startswith("."):
                continue

            if (
                file.is_file()
                and file.suffix.lower()
                in [".jpg", ".jpeg",
                    ".png", ".webp"]
            ):

                destination = (
                    processed_path
                    / file.name
                )

                count = 1

                while destination.exists():

                    destination = (
                        processed_path
                        / f"{file.stem}_{count}"
                          f"{file.suffix}"
                    )

                    count += 1

                shutil.move(
                    str(file),
                    destination
                )

        # 4. Process each image

        for file in processed_path.glob("*"):

            

            uploaded = upload_dataset_image(
                file,
                event_id
            )



            image_data = ImageSchema(

                event_id=event_id,

                image_url=uploaded[
                    "image_url"
                ],

                public_id=uploaded[
                    "public_id"
                ],

                image_name=file.name
            )



            image_id = insert_image_db(
                image_data
            )



            embedding_vectors = generate_single_image_embedding(

                image_path=file,
                image_id=image_id
            )

            if (
                embedding_vectors
                and len(embedding_vectors) > 0
            ):

                store_embedding(
                    image_id,
                    event_id,
                    embedding_vectors[0]
                )   

            else:

                print(
                    f"No embeddings generated "
                    f"for image: {image_id}"
                )

        return {
            "message":
            "Dataset uploaded successfully",

            "event_id": event_id
        }

    except Exception as e:

        print("UPLOAD FOLDER ERROR:")
        print(e)

        return {
            "error": str(e)
        }

    finally:

        # Cleanup ZIP

        try:

            if (
                temp_zip_path
                and temp_zip_path.exists()
            ):

                temp_zip_path.unlink()

        except Exception as e:

            print("ZIP CLEANUP ERROR:")
            print(e)

        # Cleanup extracted folder

        try:

            if (
                temp_extract_path
                and temp_extract_path.exists()
            ):

                shutil.rmtree(
                    temp_extract_path
                )

        except Exception as e:

            print("EXTRACT CLEANUP ERROR:")
            print(e)

        # Cleanup processed folder

        try:

            if (
                processed_path
                and processed_path.exists()
            ):

                shutil.rmtree(
                    processed_path
                )

        except Exception as e:

            print("PROCESSED CLEANUP ERROR:")
            print(e)