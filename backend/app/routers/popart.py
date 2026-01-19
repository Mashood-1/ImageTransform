from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
import tempfile
import os

from app.services.popart_service import convert_to_popart

router = APIRouter(
    prefix="/pop-art",
    tags=["Pop Art"]
)

def cleanup_files(*paths):
    for path in paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

@router.post("/")
async def generate_popart(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    suffix = ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_input:
        tmp_input.write(await file.read())
        tmp_input_path = tmp_input.name

    tmp_output_path = tmp_input_path + "_out.png"

    try:
        convert_to_popart(tmp_input_path, tmp_output_path)

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
        cleanup_files(tmp_input_path, tmp_output_path)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate Pop Art: {str(e)}"
        )
