# --- DEPENDENCIAS ---
from pathlib import Path

import pandas as pd
from PIL import Image
from PIL import ImageDraw

from config.nourishbot_config import EXAMPLES_DIR
from data.nourishbot_dataset import NOURISHBOT_MEALS


def _image_path(file_name: str) -> Path:
    return EXAMPLES_DIR / file_name


def _draw_meal(meal: dict, image_path: str | Path) -> Path:
    path = Path(image_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (480, 360), meal["background"])
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((55, 45, 425, 315), radius=56, fill=meal["plate_color"], outline="#D8D4CF", width=4)
    draw.text((30, 18), meal["title"], fill="#2B2B2B")

    if meal["image_key"] == "salmon_power_bowl":
        draw.ellipse((120, 115, 260, 245), fill="#E48860")
        draw.arc((120, 115, 260, 245), start=205, end=330, fill="#F8C4A8", width=7)
        draw.ellipse((265, 120, 365, 220), fill="#7FBF6D")
        draw.ellipse((155, 245, 295, 295), fill="#9C7448")
        draw.ellipse((300, 220, 350, 270), fill="#7DB56E")
        draw.ellipse((330, 175, 350, 195), fill="#D95252")
    elif meal["image_key"] == "veggie_buddha_bowl":
        draw.ellipse((125, 115, 365, 285), fill="#A6C96B")
        draw.ellipse((145, 135, 220, 205), fill="#E7C89D")
        draw.ellipse((240, 125, 330, 215), fill="#F09C53")
        draw.ellipse((225, 210, 320, 275), fill="#F3F2E7")
        draw.ellipse((300, 145, 350, 195), fill="#6CC070")
    else:
        draw.rounded_rectangle((130, 130, 330, 250), radius=26, fill="#D98B54")
        draw.ellipse((140, 115, 330, 205), fill="#6FAF59")
        draw.ellipse((175, 210, 330, 280), fill="#A27B4E")
        draw.rectangle((110, 140, 150, 240), fill="#E26E46")
        draw.rectangle((320, 135, 360, 230), fill="#F0C34D")

    image.save(path, format="PNG")
    return path


def ensure_example_assets() -> dict[str, Path]:
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    image_paths = {}
    for meal in NOURISHBOT_MEALS:
        path = _image_path(meal["file_name"])
        if not path.exists():
            _draw_meal(meal, path)
        image_paths[meal["image_key"]] = path
    return image_paths


def build_meal_dataset(image_processor) -> pd.DataFrame:
    assets = ensure_example_assets()
    rows = []
    for meal in NOURISHBOT_MEALS:
        file_path = assets[meal["image_key"]]
        rows.append(
            {
                **meal,
                "file_path": str(file_path),
                "Embedding": image_processor.build_embedding_for_path(file_path),
            }
        )
    return pd.DataFrame(rows)