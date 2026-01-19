# backend/app/routers/style_transfer.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.concurrency import run_in_threadpool
from PIL import Image
import io
import traceback

from app.services.style_transfer_service import convert_style_transfer

router = APIRouter(prefix="/style-transfer", tags=["Style Transfer"])


@router.post("/{style_name}/")
async def style_transfer(style_name: str, file: UploadFile = File(...)):
    try:
        # 1. Read uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # 2. Run heavy AI inference in threadpool
        output_image = await run_in_threadpool(
            convert_style_transfer,
            image,
            style_name
        )

        # 3. Convert PIL image → bytes
        img_bytes = io.BytesIO()
        output_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # 4. Return image response
        return StreamingResponse(
            img_bytes,
            media_type="image/png"
        )

    except Exception as e:
        # CRITICAL: expose error during development
        print("STYLE TRANSFER ERROR:")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
