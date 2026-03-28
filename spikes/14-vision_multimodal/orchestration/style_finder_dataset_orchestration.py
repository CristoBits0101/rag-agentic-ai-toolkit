# --- DEPENDENCIAS ---
import pandas as pd

from data.style_finder_fashion_dataset import STYLE_FINDER_OUTFITS
from orchestration.style_finder_asset_orchestration import ensure_style_finder_example_assets


def build_style_finder_dataset(image_processor) -> pd.DataFrame:
    image_paths = ensure_style_finder_example_assets()
    rows = []

    for outfit in STYLE_FINDER_OUTFITS:
        image_path = image_paths[outfit["image_key"]]
        embedding = image_processor.build_embedding_for_path(image_path)

        for item in outfit["items"]:
            rows.append(
                {
                    "Image Key": outfit["image_key"],
                    "Image Path": str(image_path),
                    "Image URL": f"file://{image_path.as_posix()}",
                    "Look Title": outfit["title"],
                    "Style": outfit["style"],
                    "Item Name": item["Item Name"],
                    "Category": item["Category"],
                    "Price": item["Price"],
                    "Source": item["Source"],
                    "Link": item["Link"],
                    "Embedding": embedding,
                }
            )

    return pd.DataFrame(rows)
