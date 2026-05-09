from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["wedding_filter"]

events_collection = db["events"]
images_collection = db["images"]

print("MongoDB Connected Successfully")