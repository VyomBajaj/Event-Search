from fastapi import FastAPI,APIRouter
from backend.routers import user_routes
from backend.routers import admin_routes
from backend.config import BASE_DIR
import backend.config
from fastapi.middleware.cors import CORSMiddleware
from backend.database import db


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




router = APIRouter()

# test_pinecone()

@app.get('/')
def home_route():
    return {"message":"Hello"}


app.include_router(user_routes.router)
app.include_router(admin_routes.router)
