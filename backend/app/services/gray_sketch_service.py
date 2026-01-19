# backend/app/services/gray_sketch_service.py

import cv2
import numpy as np

def convert_to_gray_sketch(img: np.ndarray) -> np.ndarray:
    """
    Converts an image (NumPy array) to a pencil-style gray sketch.

    Args:
        img (np.ndarray): Input image in BGR color space

    Returns:
        np.ndarray: Grayscale sketch image
    """
    if img is None:
        raise ValueError("Input image is None")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale
    inverted = 255 - gray

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)

    # Blend using color dodge
    sketch = cv2.divide(gray, 255 - blurred, scale=256)

    return sketch
