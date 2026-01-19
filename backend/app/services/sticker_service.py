# backend/app/services/sticker_service.py

from rembg import remove
from PIL import Image
import io
import os
from pathlib import Path

# Resolve bundled model path
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "u2net.onnx"

# Ensure rembg sees the model path
os.environ["RMBG_MODEL"] = str(MODEL_PATH)

def convert_to_sticker(pil_img: Image.Image) -> Image.Image:
    """
    Converts a PIL image to a sticker by removing its background.
    Uses bundled U²-Net model.
    Returns RGBA image with transparent background.
    """

    if pil_img.mode != "RGBA":
        pil_img = pil_img.convert("RGBA")

    # Convert PIL image to bytes
    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")
    buffer.seek(0)

    # Background removal
    result_bytes = remove(buffer.read())

    # Convert result back to PIL Image
    result_img = Image.open(io.BytesIO(result_bytes)).convert("RGBA")
    return result_img
