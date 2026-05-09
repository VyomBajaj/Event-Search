from pydantic import BaseModel


class ImageSchema(BaseModel):

    event_id: str

    image_url: str

    public_id: str

    image_name: str