# backend/app/services/neon_glow_service.py

from PIL import Image, ImageFilter, ImageChops
import numpy as np
import cv2

def get_vibrant_neon_color(bgr_color):
    """
    Maps an original BGR color to a vibrant neon equivalent.
    
    Args:
        bgr_color: BGR tuple from the original image
        
    Returns:
        BGR tuple for vibrant neon color
    """
    b, g, r = bgr_color
    
    # Convert BGR to HSV for better color understanding
    color_array = np.uint8([[[b, g, r]]])
    hsv = cv2.cvtColor(color_array, cv2.COLOR_BGR2HSV)[0, 0]
    h, s, v = hsv
    
    # Map hue ranges to vibrant neon colors (in BGR format)
    neon_colors = {
        # Red hues (0-15, 165-180)
        'red': (0, 0, 255),
        # Orange hues (15-30)
        'orange': (0, 165, 255),
        # Yellow hues (30-45)
        'yellow': (0, 255, 255),
        # Green hues (45-90)
        'green': (0, 255, 0),
        # Cyan hues (90-110)
        'cyan': (255, 255, 0),
        # Blue hues (110-150)
        'blue': (255, 0, 0),
        # Magenta/Pink hues (150-180)
        'pink': (255, 0, 255),
    }
    
    # Determine which neon color based on hue
    if h < 15 or h > 165:
        return neon_colors['red']
    elif h < 30:
        return neon_colors['orange']
    elif h < 45:
        return neon_colors['yellow']
    elif h < 90:
        return neon_colors['green']
    elif h < 110:
        return neon_colors['cyan']
    elif h < 150:
        return neon_colors['blue']
    else:
        return neon_colors['pink']


def convert_to_neon_glow(input_path: str, output_path: str, use_color_mapping=True) -> None:
    """
    Converts an image to a realistic neon glow sign effect with vibrant, 
    multi-colored neon tubes based on original image colors.
    
    Args:
        input_path: Path to the input image
        output_path: Path to save the neon glow result
        use_color_mapping: If True, map colors to vibrant neon equivalents
    """
    # --- Read image ---
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Cannot read image at {input_path}")
    
    if img.size == 0:
        raise ValueError("Image is empty or corrupted")
    
    # --- Step 1: Convert to grayscale for edge detection ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # --- Step 2: Apply bilateral filter to smooth while preserving edges ---
    gray_smooth = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
    
    # --- Step 3: Detect edges with Canny ---
    edges = cv2.Canny(gray_smooth, threshold1=50, threshold2=150)
    
    # --- Step 4: Dilate edges for thicker neon lines ---
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    edges_thick = cv2.dilate(edges, kernel, iterations=2)
    
    # --- Step 5: Create dark background ---
    h, w = img.shape[:2]
    dark_bg = np.zeros((h, w, 3), dtype=np.uint8)
    
    # --- Step 6: Create color-mapped neon layer ---
    neon_layer = dark_bg.copy()
    
    if use_color_mapping:
        # Map each edge pixel to a vibrant neon color based on nearby original color
        edge_indices = np.where(edges_thick != 0)
        for y, x in zip(edge_indices[0], edge_indices[1]):
            # Get original color near this edge
            original_color = img[y, x]
            # Map to vibrant neon color
            neon_color = get_vibrant_neon_color(original_color)
            neon_layer[y, x] = neon_color
    else:
        # Fallback to single cyan color
        neon_layer[edges_thick != 0] = (255, 255, 0)
    
    # --- Step 7: Create intense glow layers ---
    neon_pil = Image.fromarray(cv2.cvtColor(neon_layer, cv2.COLOR_BGR2RGB))
    
    # Multiple glow layers for intense neon effect
    glow_intense = neon_pil.filter(ImageFilter.GaussianBlur(radius=8))
    glow_medium = neon_pil.filter(ImageFilter.GaussianBlur(radius=15))
    glow_soft = neon_pil.filter(ImageFilter.GaussianBlur(radius=25))
    
    # Combine glow layers
    result = ImageChops.add(glow_intense, glow_medium)
    result = ImageChops.add(result, glow_soft)
    result = ImageChops.add(result, neon_pil)  # Add sharp neon strokes
    
    # --- Step 8: Add extra glow for intensity ---
    extra_glow = neon_pil.filter(ImageFilter.GaussianBlur(radius=35))
    result = ImageChops.add(result, extra_glow)
    
    # --- Step 9: Save result ---
    result.save(output_path, format="PNG")
