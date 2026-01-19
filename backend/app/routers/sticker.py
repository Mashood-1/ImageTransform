# backend/app/routers/sticker.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
from app.services.sticker_service import convert_to_sticker
from app.utils.image_io import read_upload_file, pil_to_bytes

router = APIRouter(
    prefix="/sticker",
    tags=["Sticker"]
)

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]

@router.post("/")
async def generate_sticker(file: UploadFile = File(...)):
    """
    Accepts an uploaded image and returns a sticker (transparent PNG).
    """
    try:
        pil_img = await read_upload_file(file)
        sticker_img = convert_to_sticker(pil_img)
        buf = pil_to_bytes(sticker_img, fmt="PNG")
        return StreamingResponse(buf, media_type="image/png")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate sticker: {str(e)}")
