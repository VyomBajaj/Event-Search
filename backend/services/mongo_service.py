from bson import ObjectId

from backend.database.db import (
    events_collection,
    images_collection
)

from backend.schemas.event_schema import EventSchema
from backend.schemas.image_schema import ImageSchema

def create_event_db(event_name):

    existing = events_collection.find_one({
        "event_name": event_name
    })

    if existing:
        return None

    event = EventSchema(
        event_name=event_name
    )

    result = events_collection.insert_one(
        event.model_dump()
    )

    return str(result.inserted_id)


def insert_image_db(image_data: ImageSchema):

    data = image_data.model_dump()

    data["event_id"] = ObjectId(
        data["event_id"]
    )

    result = images_collection.insert_one(data)

    return str(result.inserted_id)


def get_image_by_name_and_event(
    image_name,
    event_id
):

    image = images_collection.find_one({
        "image_name": image_name,
        "event_id": ObjectId(event_id)
    })

    return image


def get_event_by_name(event_name):

    try:

        if not event_name:
            return None

        event = events_collection.find_one({
            "event_name": event_name
        })

        return event

    except Exception as e:

        print("GET EVENT ERROR:")
        print(e)

        return None
    
 


def get_image_by_id(image_id):

    try:

        image = images_collection.find_one({
            "_id": ObjectId(image_id)
        })

        return image

    except Exception as e:

        print("GET IMAGE BY ID ERROR:")
        print(e)

        return None