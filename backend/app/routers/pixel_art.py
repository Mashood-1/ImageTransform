from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.concurrency import run_in_threadpool
from PIL import Image
from io import BytesIO
from fastapi.responses import StreamingResponse

from app.services.pixel_art_service import convert_pixel_art, VALID_PIXEL_STYLES

router = APIRouter(prefix="/pixel-art", tags=["Pixel Art"])

@router.post("/{style_name}/")
async def pixel_art(style_name: str, file: UploadFile = File(...)):
    """
    Apply Pixel Art filter to uploaded image.
    Supports styles: 8bit, 16bit, modern, mosaic
    """
    style_name = style_name.lower()
    if style_name not in VALID_PIXEL_STYLES:
        raise HTTPException(status_code=400, detail=f"Invalid pixel art style '{style_name}'")

    try:
        # Load image
        img_bytes = await file.read()
        pil_img = Image.open(BytesIO(img_bytes)).convert("RGB")

        # Run pixel art conversion in threadpool
        output_img = await run_in_threadpool(convert_pixel_art, pil_img, style_name)

        # Convert PIL image to BytesIO and return as streaming response
        buf = BytesIO()
        output_img.save(buf, format="PNG")
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pixel art conversion failed: {str(e)}")
