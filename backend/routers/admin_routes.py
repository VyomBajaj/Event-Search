from fastapi import Form, APIRouter,UploadFile,File
from backend.config import UPLOAD_DIR,DATA_DIR
from pathlib import Path
import tempfile
import shutil
import zipfile
from utils.generate_folder_embeddings import generate_folder_embeddings
router = APIRouter(prefix='/admin')


@router.post('/create-event')
async def create_event(event: str = Form(...)):

    event_path = DATA_DIR / event

    # check if already exists
    if event_path.exists():
        return {
            "message": "Event already exists",
            "event": event
        }

    # create folder
    event_path.mkdir(parents=True, exist_ok=True)

    # To return password will make later when we add DB

    return {
        "message": "Event created successfully",
        "event": event
    }

@router.post('/upload-folder')
async def upload_folder(
    event: str = Form(...),
    zip_file: UploadFile = File(...)
):
    event_path = DATA_DIR / event
    event_path.mkdir(parents=True, exist_ok=True)

    # 1. Save zip temporarily
    temp_zip_path = Path(tempfile.gettempdir()) / zip_file.filename

    with open(temp_zip_path, "wb") as buffer:
        shutil.copyfileobj(zip_file.file, buffer)

    # 2. Extract to temp folder
    temp_extract_path = Path(tempfile.mkdtemp())

    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_extract_path)

    # 3. Flatten files
    for file in temp_extract_path.rglob("*"):
        if file.name.startswith("."):
            continue
        if file.is_file() and file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:

            destination = event_path / file.name

            # handle duplicate names
            count = 1
            while destination.exists():
                destination = event_path / f"{file.stem}_{count}{file.suffix}"
                count += 1

            shutil.move(str(file), destination)

    # 4. Cleanup
    shutil.rmtree(temp_extract_path)
    temp_zip_path.unlink()

    # 5. Generate embeddings
    generate_folder_embeddings(event_path)

    return {
        "message": "Images uploaded, flattened, and embeddings created successfully",
        "event": event
    }