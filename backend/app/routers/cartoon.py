from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pathlib import Path
from app.services.cartoon_service import convert_to_cartoon
import tempfile
import os

router = APIRouter(
    prefix="/cartoon",
    tags=["Cartoon"]
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
            # Never raise cleanup errors
            pass


@router.post("/")
async def generate_cartoon(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    # Save uploaded file to a temporary path
    suffix = Path(file.filename).suffix or ".png"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_input:
        tmp_input.write(await file.read())
        tmp_input_path = tmp_input.name

    # Output temp file
    tmp_output_path = tmp_input_path + "_out.png"

    try:
        # Generate cartoon
        convert_to_cartoon(tmp_input_path, tmp_output_path)

        # Schedule cleanup AFTER response is sent
        background_tasks.add_task(
            cleanup_files,
            tmp_input_path,
            tmp_output_path
        )

        return StreamingResponse(
            open(tmp_output_path, "rb"),
            media_type="image/png"
        )

    except Exception as e:
        # Cleanup immediately if something fails
        cleanup_files(tmp_input_path, tmp_output_path)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate cartoon: {str(e)}"
        )
