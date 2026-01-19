# backend/app/routers/gray_sketch.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

from app.services.gray_sketch_service import convert_to_gray_sketch
from app.utils.image_io import (
    read_upload_file,
    pil_to_cv,
    cv_to_png_bytes
)

router = APIRouter(
    prefix="/gray-sketch",
    tags=["Gray Sketch"]
)


@router.post("/")
async def generate_gray_sketch(file: UploadFile = File(...)):
    """
    Accepts an uploaded image and returns a grayscale pencil sketch.
    Supports jpg, png, webp.
    """
    try:
        # --- Read and validate image ---
        pil_img = await read_upload_file(file)

        # --- Convert to OpenCV BGR ---
        cv_img = pil_to_cv(pil_img)

        # --- Process image ---
        sketch_array = convert_to_gray_sketch(cv_img)

        # --- Encode result ---
        buf = cv_to_png_bytes(sketch_array)

        return StreamingResponse(buf, media_type="image/png")

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate gray sketch: {str(e)}"
        )
