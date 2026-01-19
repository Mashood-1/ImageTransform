# backend/app/services/color_sketch_service.py

import cv2
import numpy as np


def convert_to_color_sketch_from_array(img: np.ndarray) -> np.ndarray:
    """
    Converts an image array (BGR) to a color pencil sketch.

    Args:
        img (np.ndarray): Input image in BGR format

    Returns:
        np.ndarray: Color pencil sketch image in BGR format
    """
    if img is None or img.size == 0:
        raise ValueError("Invalid input image")

    # --- Step 1: Smooth colors while preserving edges ---
    color_smooth = cv2.bilateralFilter(img, d=9, sigmaColor=90, sigmaSpace=90)

    # --- Step 2: Reduce saturation for sketch appearance ---
    hsv = cv2.cvtColor(color_smooth, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] *= 0.7
    hsv = np.clip(hsv, 0, 255).astype(np.uint8)
    color_sketch = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # --- Step 3: Edge detection ---
    gray = cv2.cvtColor(color_sketch, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)

    # --- Step 4: Pencil stroke texture ---
    pencil_strokes = 255 - edges_dilated
    pencil_strokes = cv2.GaussianBlur(pencil_strokes, (5, 5), 1.0)

    # --- Step 5: Cross-hatching texture ---
    h, w = img.shape[:2]

    hatching_1 = np.zeros((h, w), dtype=np.uint8)
    for i in range(0, h, 4):
        cv2.line(hatching_1, (0, i), (w, i + w), 200, 1)

    hatching_2 = np.zeros((h, w), dtype=np.uint8)
    for i in range(-w, h, 4):
        cv2.line(hatching_2, (0, i), (w, i + w), 180, 1)

    hatching = cv2.bitwise_or(hatching_1, hatching_2)
    hatching = cv2.GaussianBlur(hatching, (3, 3), 0)

    # --- Step 6: Blend strokes and texture ---
    edge_strength = cv2.cvtColor(pencil_strokes, cv2.COLOR_GRAY2BGR).astype(np.float32) / 255.0
    hatching_3ch = cv2.cvtColor(hatching, cv2.COLOR_GRAY2BGR).astype(np.float32) / 255.0

    texture = edge_strength * 0.6 + hatching_3ch * 0.4
    texture = np.clip(texture, 0, 1)

    # --- Step 7: Apply texture ---
    color_float = color_sketch.astype(np.float32)
    result = color_float * texture * 0.95 + color_float * 0.05
    result = np.clip(result - 15, 0, 255).astype(np.uint8)

    return result


# -------------------------------------------------------------------
# TEMPORARY COMPATIBILITY LAYER (DO NOT REMOVE YET)
# -------------------------------------------------------------------

def convert_to_color_sketch(image_path: str) -> np.ndarray:
    """
    Compatibility wrapper.
    This will be removed once the router is refactored.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image at {image_path}")

    return convert_to_color_sketch_from_array(img)
