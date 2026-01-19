# backend/app/utils/image_io.py

from PIL import Image
import io
import numpy as np
import cv2
from fastapi import UploadFile

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]


async def read_upload_file(upload_file: UploadFile) -> Image.Image:
    """
    Reads a FastAPI UploadFile and returns a PIL Image.
    Preserves alpha if present.
    """
    if upload_file.content_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Unsupported file type: {upload_file.content_type}")

    contents = await upload_file.read()
    if not contents:
        raise ValueError("Uploaded file is empty")

    pil_img = Image.open(io.BytesIO(contents))

    # Normalize image mode
    if pil_img.mode not in ("RGB", "RGBA"):
        pil_img = pil_img.convert("RGB")

    return pil_img


def pil_to_cv(pil_img: Image.Image) -> np.ndarray:
    """
    Converts a PIL Image to an OpenCV NumPy array.
    Handles RGB and RGBA correctly.
    """
    img_array = np.array(pil_img)

    if pil_img.mode == "RGBA":
        return cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGRA)

    return cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)


def cv_to_pil(cv_img: np.ndarray) -> Image.Image:
    """
    Converts an OpenCV NumPy array to a PIL Image.
    Handles BGR, BGRA, and GRAY images.
    """
    if len(cv_img.shape) == 2:
        return Image.fromarray(cv_img).convert("RGB")

    if cv_img.shape[2] == 4:
        return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGRA2RGBA))

    return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))


def pil_to_bytes(pil_img: Image.Image, fmt: str = "PNG") -> io.BytesIO:
    """
    Converts a PIL Image to a BytesIO buffer.
    """
    buf = io.BytesIO()
    pil_img.save(buf, format=fmt)
    buf.seek(0)
    return buf


def cv_to_png_bytes(cv_img: np.ndarray) -> io.BytesIO:
    """
    Converts an OpenCV image directly to PNG bytes.
    """
    pil_img = cv_to_pil(cv_img)
    return pil_to_bytes(pil_img)
