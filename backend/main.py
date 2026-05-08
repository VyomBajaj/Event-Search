from fastapi import FastAPI,APIRouter
from fastapi.staticfiles import StaticFiles
from backend.routers import user_routes
from backend.routers import admin_routes
from backend.config import BASE_DIR
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR/'data'),
    name="static"
)


router = APIRouter()

@app.get('/')
def home_route():
    return {"message":"Hello"}

app.include_router(user_routes.router)
app.include_router(admin_routes.router)
