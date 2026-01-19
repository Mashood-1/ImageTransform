# backend/app/services/popart_service.py

import cv2
import numpy as np
import os

def convert_to_popart(input_path: str, output_path: str) -> None:
    """
    Converts an input image to Pop Art / Warhol style.
    Posterized colors, high contrast, optional repeated panels.
    """
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Failed to read input image")

    # Resize to a manageable size for processing
    h, w = img.shape[:2]
    scale = 512 / max(h, w)
    img = cv2.resize(img, (int(w * scale), int(h * scale)))

    # Posterize colors: reduce to 4–6 levels per channel
    levels = 4
    img_posterized = (img // (256 // levels)) * (256 // levels)

    # Optional: increase contrast
    lab = cv2.cvtColor(img_posterized, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    lab = cv2.merge([l, a, b])
    img_contrast = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Optional: replicate 2x2 panels with different color tints
    h, w = img_contrast.shape[:2]
    canvas = np.zeros((h*2, w*2, 3), dtype=np.uint8)

    # Apply different color maps for each panel
    canvas[0:h, 0:w] = cv2.applyColorMap(img_contrast, cv2.COLORMAP_JET)
    canvas[0:h, w:2*w] = cv2.applyColorMap(img_contrast, cv2.COLORMAP_HSV)
    canvas[h:2*h, 0:w] = cv2.applyColorMap(img_contrast, cv2.COLORMAP_OCEAN)
    canvas[h:2*h, w:2*w] = cv2.applyColorMap(img_contrast, cv2.COLORMAP_PINK)

    cv2.imwrite(output_path, canvas)

    # Clean up temp input
    if os.path.exists(input_path):
        try:
            os.remove(input_path)
        except Exception:
            pass
