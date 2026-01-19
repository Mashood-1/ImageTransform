import numpy as np
from PIL import Image
from typing import Dict

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

VALID_PIXEL_STYLES = ["8bit", "16bit", "modern", "mosaic"]

# Style presets (tuned for visual quality)
STYLE_PRESETS: Dict[str, Dict] = {
    "8bit": {
        "scale": 0.08,
        "colors": 12
    },
    "16bit": {
        "scale": 0.12,
        "colors": 24
    },
    "modern": {
        "scale": 0.18,
        "colors": 48
    },
    "mosaic": {
        "scale": 0.05,
        "colors": 8
    }
}

# -------------------------------------------------------------------
# Helper: resize image (pixelation)
# -------------------------------------------------------------------

def pixelate_image(pil_img: Image.Image, scale: float) -> Image.Image:
    """
    Downscale then upscale image to create pixel blocks.
    """
    w, h = pil_img.size
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    small = pil_img.resize((new_w, new_h), Image.NEAREST)
    pixelated = small.resize((w, h), Image.NEAREST)
    return pixelated

# -------------------------------------------------------------------
# Helper: reduce color palette
# -------------------------------------------------------------------

def reduce_colors(pil_img: Image.Image, colors: int) -> Image.Image:
    """
    Reduce image to a limited color palette.
    """
    return pil_img.convert(
        "P",
        palette=Image.ADAPTIVE,
        colors=colors
    ).convert("RGB")

# -------------------------------------------------------------------
# Main service function
# -------------------------------------------------------------------

def convert_pixel_art(pil_img: Image.Image, style_name: str) -> Image.Image:
    """
    Apply pixel art effect to a PIL image.
    Returns a PIL image.
    """
    try:
        if style_name not in VALID_PIXEL_STYLES:
            raise ValueError(f"Invalid pixel art style '{style_name}'")

        preset = STYLE_PRESETS[style_name]

        # Ensure RGB
        pil_img = pil_img.convert("RGB")

        # Pixelation
        pixelated = pixelate_image(
            pil_img,
            scale=preset["scale"]
        )

        # Color reduction
        final_img = reduce_colors(
            pixelated,
            colors=preset["colors"]
        )

        return final_img

    except Exception as e:
        raise RuntimeError(
            f"Pixel art conversion failed for style '{style_name}': {str(e)}"
        )
