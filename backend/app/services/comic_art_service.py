# backend/app/services/comic_art_service.py

import cv2
import numpy as np
import os

def convert_to_comic_art(input_path: str, output_path: str) -> None:
    """
    Converts an image to a comic-style effect:
    - Bold outlines
    - Posterized flat colors
    """
    # --- Step 1: Read image ---
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Failed to read input image")

    # Convert to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # --- Step 2: Edge detection (bold) ---
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Laplacian(gray_blur, cv2.CV_8U, ksize=5)
    _, edges_binary = cv2.threshold(edges, 80, 255, cv2.THRESH_BINARY_INV)

    # --- Step 3: Posterize colors ---
    # Reduce to 6 colors using k-means
    data = img_rgb.reshape((-1, 3)).astype(np.float32)
    K = 6
    _, labels, centers = cv2.kmeans(
        data, K, None,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001),
        10,
        cv2.KMEANS_RANDOM_CENTERS
    )
    centers = np.uint8(centers)
    posterized = centers[labels.flatten()].reshape(img_rgb.shape)

    # --- Step 4: Combine edges and posterized colors ---
    edges_rgb = cv2.cvtColor(edges_binary, cv2.COLOR_GRAY2RGB)
    comic = cv2.bitwise_and(posterized, edges_rgb)

    # --- Step 5: Save output ---
    cv2.imwrite(output_path, cv2.cvtColor(comic, cv2.COLOR_RGB2BGR))

    # Optional: delete input
    if os.path.exists(input_path):
        try:
            os.remove(input_path)
        except Exception:
            pass
