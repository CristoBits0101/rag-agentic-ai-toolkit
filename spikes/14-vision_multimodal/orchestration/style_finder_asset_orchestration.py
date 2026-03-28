# --- DEPENDENCIAS ---
from pathlib import Path

from PIL import Image
from PIL import ImageDraw

from config.style_finder_fashion_config import STYLE_FINDER_EXAMPLES_DIR
from data.style_finder_fashion_dataset import STYLE_FINDER_OUTFITS


def build_example_image_path(file_name: str) -> Path:
    return STYLE_FINDER_EXAMPLES_DIR / file_name


def draw_outfit_example_image(outfit: dict, image_path: str | Path) -> Path:
    path = Path(image_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (420, 540), outfit["background"])
    draw = ImageDraw.Draw(image)
    center_x = 210
    draw.ellipse((160, 40, 260, 140), fill="#F0D2B3")
    draw.rectangle((175, 135, 245, 195), fill=outfit["garments"]["top"]["color"])
    draw.rounded_rectangle((125, 145, 295, 305), radius=18, fill=outfit["garments"]["outerwear"]["color"])
    draw.rectangle((165, 305, 255, 470), fill=outfit["garments"]["bottom"]["color"])
    draw.rectangle((158, 470, 193, 520), fill=outfit["garments"]["shoes"]["color"])
    draw.rectangle((227, 470, 262, 520), fill=outfit["garments"]["shoes"]["color"])
    draw.text((24, 24), outfit["title"], fill="#FFFFFF")
    draw.text((24, 56), outfit["style"], fill="#FFFFFF")
    draw.text((24, 496), outfit["garments"]["outerwear"]["label"], fill="#FFFFFF")
    image.save(path, format="PNG")
    return path


def ensure_style_finder_example_assets() -> dict[str, Path]:
    image_paths = {}

    for outfit in STYLE_FINDER_OUTFITS:
        image_path = build_example_image_path(outfit["file_name"])
        if not image_path.exists():
            draw_outfit_example_image(outfit, image_path)

        image_paths[outfit["image_key"]] = image_path

    return image_paths
