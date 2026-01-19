from pathlib import Path
from app.services.cartoon_service import convert_to_cartoon

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_IMAGE = BASE_DIR / "jpegls-home.jpg"
OUTPUT_IMAGE = BASE_DIR / "sample_output.png"

if __name__ == "__main__":
    convert_to_cartoon(
        input_path=str(INPUT_IMAGE),
        output_path=str(OUTPUT_IMAGE)
    )

    print("Cartoon image generated:", OUTPUT_IMAGE)
