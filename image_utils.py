import uuid
from pathlib import Path

from PIL import Image, ImageOps
from io import BytesIO


PROFILE_PICs_DIR = Path("media/profile_pics")

# image processing
def process_profile_image(content: bytes) -> str:

    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)

        img = ImageOps.fit(img, (300,300), method= Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA" , "P"):
            img = img.convert("RGB")

        filename = f"{uuid.uuid4().hex}.jpg"

        filepath = PROFILE_PICs_DIR / filename

        PROFILE_PICs_DIR.mkdir(parents= True , exist_ok=True)

        img.save(filepath, "JPEG", quality=85 , optimize= True)

    return filename



# delete image
def delete_profile_image(filename: str | None)-> None:
    if filename is None:
        return

    filepath = PROFILE_PICs_DIR/filename

    if filepath.exists():
        filepath.unlink()