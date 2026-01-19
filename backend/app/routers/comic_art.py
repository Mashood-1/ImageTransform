# backend/app/routers/comic_art.py

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from app.services.comic_art_service import convert_to_comic_art
from pathlib import Path
import tempfile
import os

router = APIRouter(
    prefix="/comic-art",
    tags=["Comic Art"]
)

def cleanup_files(*paths):
    """
    Safely delete temporary files after the response is fully sent.
    Works correctly on Windows and Linux.
    """
    for path in paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

@router.post("/")
async def generate_comic_art(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    # Determine file extension
    suffix = Path(file.filename).suffix or ".png"

    # Save uploaded file to temporary path
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_input:
        tmp_input.write(await file.read())
        tmp_input_path = tmp_input.name

    tmp_output_path = tmp_input_path + "_out.png"

    try:
        # Process image
        convert_to_comic_art(tmp_input_path, tmp_output_path)

        # Schedule cleanup after response
        background_tasks.add_task(cleanup_files, tmp_input_path, tmp_output_path)

        return StreamingResponse(
            open(tmp_output_path, "rb"),
            media_type="image/png"
        )

    except Exception as e:
        cleanup_files(tmp_input_path, tmp_output_path)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate comic art: {str(e)}"
        )
