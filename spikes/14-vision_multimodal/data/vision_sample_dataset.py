# --- DEPENDENCIAS ---
from dataclasses import dataclass

# --- DATA ---
@dataclass(frozen=True)
class VisionSampleRecord:
    image_id: str
    image_url: str
    description: str
    object_counts: dict[str, int]
    attributes: dict[str, str]
    text_fields: dict[str, str]
    vector_terms: tuple[str, ...]


@dataclass(frozen=True)
class CatalogItem:
    item_name: str
    price: float
    link: str
    vector_terms: tuple[str, ...]


VISION_SAMPLE_RECORDS = {
    "cat_window": VisionSampleRecord(
        image_id="cat_window",
        image_url="https://images.local/cat_window.jpg",
        description=(
            "The image shows an orange cat sitting on a windowsill and looking outside at daylight."
        ),
        object_counts={"cat": 1, "window": 1},
        attributes={"cat_color": "orange"},
        text_fields={},
        vector_terms=("cat", "orange", "window", "indoor", "pet"),
    ),
    "city_scene": VisionSampleRecord(
        image_id="city_scene",
        image_url="https://images.local/city_scene.jpg",
        description=(
            "The photo shows a city street with three cars near a crosswalk and a woman wearing a red jacket."
        ),
        object_counts={"cars": 3, "woman": 1, "crosswalk": 1},
        attributes={"woman_jacket_color": "red"},
        text_fields={},
        vector_terms=("city", "street", "cars", "woman", "red", "jacket", "urban"),
    ),
    "fashion_outfit": VisionSampleRecord(
        image_id="fashion_outfit",
        image_url="https://images.local/fashion_outfit.jpg",
        description=(
            "The image shows a business casual outfit with a navy blazer white blouse and black trousers."
        ),
        object_counts={"person": 1, "blazer": 1, "blouse": 1, "trousers": 1},
        attributes={
            "style": "business casual",
            "primary_color": "navy",
            "top": "white blouse",
            "outerwear": "navy blazer",
            "bottom": "black trousers",
        },
        text_fields={},
        vector_terms=(
            "fashion",
            "business",
            "casual",
            "navy",
            "white",
            "black",
            "blazer",
            "blouse",
            "trousers",
        ),
    ),
    "nutrition_label": VisionSampleRecord(
        image_id="nutrition_label",
        image_url="https://images.local/nutrition_label.jpg",
        description=(
            "The image contains a nutrition label for a packaged food product with calories sodium protein and carbohydrate values."
        ),
        object_counts={"label": 1},
        attributes={"category": "nutrition facts"},
        text_fields={
            "calories": "230",
            "protein": "5 g",
            "carbohydrates": "37 g",
            "fat": "8 g",
            "sodium": "470 mg",
            "vitamin_c": "10 percent",
        },
        vector_terms=("food", "label", "nutrition", "sodium", "calories", "packaged"),
    ),
}


FASHION_CATALOG_ITEMS = [
    CatalogItem(
        item_name="Navy blazer with white blouse and black trousers",
        price=129.0,
        link="https://catalog.local/navy-blazer-look",
        vector_terms=(
            "fashion",
            "business",
            "casual",
            "navy",
            "white",
            "black",
            "blazer",
            "blouse",
            "trousers",
        ),
    ),
    CatalogItem(
        item_name="Olive overshirt with beige chinos",
        price=89.0,
        link="https://catalog.local/olive-overshirt-look",
        vector_terms=("fashion", "casual", "olive", "beige", "overshirt", "chinos"),
    ),
    CatalogItem(
        item_name="Black dress with silver belt",
        price=149.0,
        link="https://catalog.local/black-dress-look",
        vector_terms=("fashion", "formal", "black", "dress", "silver"),
    ),
]
