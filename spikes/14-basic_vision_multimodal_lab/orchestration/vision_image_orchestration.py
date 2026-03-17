# --- DEPENDENCIAS ---
import base64
import json
from pathlib import Path

from data.vision_sample_dataset import VISION_SAMPLE_RECORDS

# --- IMAGE ---
def encode_image_bytes(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def input_image_setup(uploaded_file) -> str:
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    return encode_image_bytes(uploaded_file.read())


def build_record_payload(image_id: str) -> bytes:
    return json.dumps({"image_id": image_id}).encode("utf-8")


def encode_image_from_url(image_url: str) -> str:
    path = Path(image_url)
    if path.exists():
        return encode_image_bytes(path.read_bytes())

    for record in VISION_SAMPLE_RECORDS.values():
        if record.image_url == image_url:
            return encode_image_bytes(build_record_payload(record.image_id))

    raise ValueError(f"Unsupported image URL: {image_url}")


def encode_images_from_urls(image_urls: list[str]) -> list[str]:
    return [encode_image_from_url(image_url) for image_url in image_urls]


def create_vision_message(prompt: str, encoded_image: str):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64," + encoded_image},
                },
            ],
        }
    ]
