from backend.database.db import events_collection

events_collection.insert_one({
    "event_name": "test_event"
})