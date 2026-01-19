# backend/app/services/manga_service.py

import cv2
import numpy as np
import os

def convert_to_manga(input_path: str, output_path: str) -> None:

    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Failed to read input image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- smooth and denoise ---
    smooth = cv2.bilateralFilter(gray, 9, 75, 75)
    smooth = cv2.medianBlur(smooth, 5)

    # --- edges ---
    edges = cv2.Canny(smooth, 80, 180)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)
    edges_inv = 255 - edges_dilated

    # --- halftone dots ---
    h, w = gray.shape
    halftone = np.ones_like(gray) * 255
    step = 4
    for y in range(0, h, step):
        for x in range(0, w, step):
            if smooth[y, x] < 128:
                radius = 1 + (128 - smooth[y, x]) // 32
                cv2.circle(halftone, (x, y), radius, 0, -1)

    # --- cross-hatching ---
    hatching = np.ones_like(gray) * 255  # start white
    hatch_step = 6
    for y in range(0, h, hatch_step):
        for x in range(0, w, hatch_step):
            if smooth[y, x] < 180:
                # 45° diagonal
                if y + hatch_step < h and x + hatch_step < w:
                    cv2.line(hatching, (x, y), (x + hatch_step, y + hatch_step), 0, 1)
                # 135° diagonal
                if y + hatch_step < h and x - hatch_step >= 0:
                    cv2.line(hatching, (x, y), (x - hatch_step, y + hatch_step), 0, 1)

    # --- combine edges, halftone, and hatching ---
    manga_final = cv2.bitwise_and(edges_inv, halftone)
    manga_final = cv2.bitwise_and(manga_final, hatching)

    # --- optional posterization ---
    manga_final = (manga_final // 32) * 32

    cv2.imwrite(output_path, manga_final)

    if os.path.exists(input_path):
        try:
            os.remove(input_path)
        except Exception:
            pass
