# backend/app/services/style_transfer_service.py

import torch
from torch import nn
from pathlib import Path
from PIL import Image
import numpy as np
import cv2

from torchvision import transforms

from app.ml.transformer_net import TransformerNet

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "models" / "instance_norm"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

VALID_STYLES = ["candy", "mosaic", "rain_princess", "udnie"]

# Style-specific max sizes (improves quality)
STYLE_MAX_SIZE = {
    "candy": 512,
    "mosaic": 512,
    "rain_princess": 512,
    "udnie": 640,
}

# Cache for loaded models
_loaded_models: dict[str, nn.Module] = {}

# -------------------------------------------------------------------
# Model loader (cached, InstanceNorm-safe)
# -------------------------------------------------------------------

def load_style_model(style_name: str) -> nn.Module:
    if style_name not in VALID_STYLES:
        raise ValueError(f"Invalid style '{style_name}'")

    if style_name in _loaded_models:
        return _loaded_models[style_name]

    model_path = MODEL_DIR / f"{style_name}.pth"
    if not model_path.exists():
        raise FileNotFoundError(f"Style model not found: {model_path}")

    model = TransformerNet().to(DEVICE)

    state_dict = torch.load(model_path, map_location=DEVICE)

    # Remove legacy InstanceNorm buffers (fixes PyTorch >=0.4 incompatibility)
    clean_state_dict = {
        k: v for k, v in state_dict.items()
        if not (
            "running_mean" in k or
            "running_var" in k or
            "num_batches_tracked" in k
        )
    }

    model.load_state_dict(clean_state_dict, strict=False)
    model.eval()

    _loaded_models[style_name] = model
    return model

# -------------------------------------------------------------------
# Image preprocessing
# -------------------------------------------------------------------

def resize_image(pil_img: Image.Image, max_size: int) -> Image.Image:
    """
    Resize image so the longest side == max_size (if needed),
    preserving aspect ratio.
    """
    w, h = pil_img.size
    if max(w, h) <= max_size:
        return pil_img

    scale = max_size / max(w, h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    return pil_img.resize((new_w, new_h), Image.LANCZOS)

# ImageNet normalization (required for these models)
_IMAGE_NET_TRANSFORM = transforms.Compose([
    transforms.ToTensor(),  # [0,1]
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])

def pil_to_tensor(pil_img: Image.Image) -> torch.Tensor:
    tensor = _IMAGE_NET_TRANSFORM(pil_img)
    return tensor.unsqueeze(0).to(DEVICE)

# -------------------------------------------------------------------
# Post-processing
# -------------------------------------------------------------------

def tensor_to_pil(tensor: torch.Tensor) -> Image.Image:
    """
    Convert model output tensor to PIL image.
    """
    tensor = tensor.squeeze(0).cpu()
    tensor = tensor.clamp(0.0, 1.0)

    img = (tensor * 255).byte()
    img = img.permute(1, 2, 0).numpy()  # HWC

    return Image.fromarray(img)

def smooth_image(pil_img: Image.Image) -> Image.Image:
    """
    Mild edge-preserving smoothing to reduce NST noise.
    """
    img = np.array(pil_img)
    img = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
    return Image.fromarray(img)

# -------------------------------------------------------------------
# Main service function
# -------------------------------------------------------------------

def convert_style_transfer(pil_img: Image.Image, style_name: str) -> Image.Image:
    """
    Apply fast neural style transfer to a PIL image.
    Returns a PIL image.
    """
    try:
        # Style-aware resizing
        max_size = STYLE_MAX_SIZE.get(style_name, 512)
        pil_img = resize_image(pil_img, max_size)

        # Load model (cached)
        model = load_style_model(style_name)

        # Convert to tensor
        input_tensor = pil_to_tensor(pil_img)

        # Inference
        with torch.no_grad():
            output_tensor = model(input_tensor)

        # Convert back to PIL
        output_img = tensor_to_pil(output_tensor)

        # Optional smoothing (recommended)
        output_img = smooth_image(output_img)

        return output_img

    except Exception as e:
        raise RuntimeError(
            f"Style transfer failed for style '{style_name}': {str(e)}"
        )
