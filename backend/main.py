from fastapi import FastAPI,APIRouter
from routers import user_routes
from routers import admin_routes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# test_pinecone()

@app.get('/')
def home_route():
    return {"message":"Hello"}

@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(user_routes.router)
app.include_router(admin_routes.router)
