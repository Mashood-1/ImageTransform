from pathlib import Path
import torch
from PIL import Image
import torchvision.transforms as T
from app.ml.animegan_generator import Generator
import os

# -------------------------------------------------------------------
# Paths & device
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "models" / "face_paint_512_v2.pt"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -------------------------------------------------------------------
# Load AnimeGANv2 generator (LOCAL, OFFLINE)
# -------------------------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"AnimeGAN model not found: {MODEL_PATH}")

_model = Generator()
state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
_model.load_state_dict(state_dict)
_model.eval()
_model.to(DEVICE)

# -------------------------------------------------------------------
# Image helpers
# -------------------------------------------------------------------

def resize_and_pad(img: Image.Image, target_size: int = 512):
    """
    Resize image so the longest side == target_size,
    then pad to (target_size, target_size) without cropping.
    """
    w, h = img.size
    scale = target_size / max(w, h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    img_resized = img.resize((new_w, new_h), Image.BICUBIC)

    canvas = Image.new("RGB", (target_size, target_size), (255, 255, 255))
    pad_x = (target_size - new_w) // 2
    pad_y = (target_size - new_h) // 2

    canvas.paste(img_resized, (pad_x, pad_y))

    return canvas, (pad_x, pad_y, new_w, new_h)

# -------------------------------------------------------------------
# Public service function
# -------------------------------------------------------------------

def convert_to_cartoon(input_path: str, output_path: str) -> None:
    """
    Convert an input image to anime/cartoon style using AnimeGANv2.
    Preserves full image content regardless of aspect ratio.
    """
    img = Image.open(input_path).convert("RGB")

    padded_img, meta = resize_and_pad(img)
    pad_x, pad_y, w, h = meta

    transform = T.Compose([
        T.ToTensor(),
        T.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])

    input_tensor = transform(padded_img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output_tensor = _model(input_tensor)

    # Denormalize
    output_tensor = (output_tensor.squeeze(0) * 0.5 + 0.5).clamp(0, 1)
    output_img = T.ToPILImage()(output_tensor)

    # Remove padding to restore original aspect
    final_img = output_img.crop(
        (pad_x, pad_y, pad_x + w, pad_y + h)
    )

    final_img.save(output_path)

    # Optionally delete temp input if needed
    if os.path.exists(input_path):
        try:
            os.remove(input_path)
        except Exception:
            pass
