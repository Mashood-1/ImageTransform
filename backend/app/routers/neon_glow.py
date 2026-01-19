from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pathlib import Path
from app.services.neon_glow_service import convert_to_neon_glow
import tempfile
import os

router = APIRouter(
    prefix="/neon-glow",
    tags=["NeonGlow"]
)

# -------------------------
# Cleanup function
# -------------------------
def cleanup_files(*paths):
    for path in paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception:
            pass

# -------------------------
# Endpoint
# -------------------------
@router.post("/")
async def generate_neon_glow(
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
        # Apply neon glow effect with color mapping
        convert_to_neon_glow(tmp_input_path, tmp_output_path, use_color_mapping=True)

        # Schedule cleanup after response is sent
        background_tasks.add_task(cleanup_files, tmp_input_path, tmp_output_path)

        # Stream result back
        with open(tmp_output_path, "rb") as f:
            result_bytes = f.read()
        return StreamingResponse(
            iter([result_bytes]),
            media_type="image/png"
        )

    except ValueError as ve:
        cleanup_files(tmp_input_path, tmp_output_path)
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image: {str(ve)}"
        )
    except Exception as e:
        print("Neon Glow Error:", e)  # Log full error
        cleanup_files(tmp_input_path, tmp_output_path)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate Neon Glow: {str(e)}"
        )
