# --- DEPENDENCIAS ---
from pathlib import Path

from PIL import Image
from PIL import ImageDraw

from config.nutrition_coach_config import NUTRITION_COACH_EXAMPLES_DIR
from data.nutrition_coach_dataset import NUTRITION_COACH_MEALS


def build_example_image_path(file_name: str) -> Path:
    return NUTRITION_COACH_EXAMPLES_DIR / file_name


def draw_meal_example_image(meal: dict, image_path: str | Path) -> Path:
    path = Path(image_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (480, 360), meal["background"])
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((55, 45, 425, 315), radius=60, fill=meal["plate_color"], outline="#D0D0D0", width=4)
    draw.text((24, 18), meal["title"], fill="#2C2C2C")

    if meal["image_key"] == "burger_combo":
        draw.rounded_rectangle((145, 135, 300, 165), radius=16, fill="#DDA45B")
        draw.rectangle((150, 165, 295, 190), fill="#4B2E20")
        draw.rectangle((155, 190, 290, 205), fill="#F6C453")
        draw.rectangle((150, 205, 295, 220), fill="#6CA24A")
        draw.rounded_rectangle((145, 220, 300, 252), radius=16, fill="#C88947")
        draw.rectangle((325, 135, 375, 255), fill="#C44D2B")
        for offset in range(0, 6):
            x = 330 + offset * 7
            draw.rectangle((x, 120 - offset * 2, x + 5, 170), fill="#F2C14E")
    elif meal["image_key"] == "salmon_plate":
        draw.ellipse((130, 120, 270, 250), fill="#E78B5B")
        draw.arc((130, 120, 270, 250), start=200, end=340, fill="#F7B28A", width=8)
        draw.ellipse((285, 125, 390, 235), fill="#8CC57A")
        for offset in range(0, 6):
            draw.line((315 + offset * 10, 135, 300 + offset * 8, 225), fill="#5F9B56", width=4)
        draw.ellipse((165, 255, 320, 305), fill="#B88A54")
    else:
        draw.ellipse((125, 100, 380, 290), fill="#A8C66C")
        draw.ellipse((165, 120, 235, 190), fill="#E7C48E")
        draw.ellipse((250, 130, 325, 205), fill="#8FCB6C")
        draw.ellipse((220, 205, 305, 265), fill="#F0F3E8")
        draw.line((220, 110, 195, 80), fill="#4C9A48", width=6)
        draw.line((290, 105, 320, 75), fill="#4C9A48", width=6)

    image.save(path, format="PNG")
    return path


def ensure_nutrition_coach_example_assets() -> dict[str, Path]:
    image_paths = {}

    for meal in NUTRITION_COACH_MEALS:
        image_path = build_example_image_path(meal["file_name"])
        if not image_path.exists():
            draw_meal_example_image(meal, image_path)

        image_paths[meal["image_key"]] = image_path

    return image_paths
