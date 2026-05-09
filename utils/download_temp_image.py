import requests
import tempfile
from pathlib import Path

def download_temp_image(image_url):

    response = requests.get(image_url)

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    )

    temp_file.write(response.content)
    temp_file.close()

    return Path(temp_file.name)