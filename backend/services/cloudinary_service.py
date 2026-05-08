import cloudinary.uploader

def upload_user_image(file, event):

    try:

        result = cloudinary.uploader.upload(
            file.file,
            folder=f"uploads/{event}"
        )

        return {
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }

    except Exception as e:
        print("CLOUDINARY ERROR:")
        print(e)

        return {
            "error": str(e)
        }