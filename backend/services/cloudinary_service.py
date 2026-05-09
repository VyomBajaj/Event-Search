import cloudinary.uploader

def upload_user_image(file, event_id):

    try:
        if not file:
            return {
                "error": "No file provided"
            }

        result = cloudinary.uploader.upload(

            file.file,

            folder=f"uploads/{event_id}"
        )

        return {

            "url":
            result.get("secure_url"),

            "public_id":
            result.get("public_id")
        }

    except Exception as e:

        print("CLOUDINARY ERROR:")
        print(e)

        return {
            "error": str(e)
        }
    

def upload_dataset_image(file_path, event_id):

    result = cloudinary.uploader.upload(
        str(file_path),
        folder=f"data/{event_id}"
    )

    return {
        "image_url": result["secure_url"],
        "public_id": result["public_id"]
    }