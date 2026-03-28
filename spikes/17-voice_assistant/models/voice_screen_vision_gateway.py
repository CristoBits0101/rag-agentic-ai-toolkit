# --- DEPENDENCIAS ---
import base64
import io
import json
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

from config.voice_desktop_config import OLLAMA_API_URL
from config.voice_desktop_config import OLLAMA_SCREEN_VISION_MODEL_CANDIDATES
from config.voice_desktop_config import SCREEN_VISION_MIN_CONFIDENCE
from models.voice_agent_ollama_gateway import extract_ollama_text
from models.voice_agent_ollama_gateway import list_installed_ollama_models
from models.voice_agent_ollama_gateway import select_best_available_ollama_model


def encode_image_to_base64(image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def build_screen_target_payload(
    model_name: str,
    target_name: str,
    target_description: str,
    encoded_image: str,
) -> dict:
    system_message = (
        "Eres un localizador visual de interfaces de escritorio. "
        "Recibes una captura de pantalla y un objetivo concreto. "
        "Devuelve solo JSON valido sin markdown. "
        "Usa coordenadas enteras en pixeles relativas a la captura completa con origen en la esquina superior izquierda. "
        "Si el objetivo no es claramente visible devuelve found en false y x e y en 0."
    )
    user_message = (
        "Objetivo permitido:\n"
        f"- id: {target_name}\n"
        f"- descripcion: {target_description}\n\n"
        "Responde con este esquema JSON exacto:\n"
        '{'
        '"found":true,'
        '"x":0,'
        '"y":0,'
        '"confidence":0.0,'
        '"reason":"motivo breve en espanol"'
        '}'
    )
    return {
        "model": model_name,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": user_message,
                "images": [encoded_image],
            },
        ],
        "options": {
            "temperature": 0,
        },
    }


def send_screen_target_request(
    payload: dict,
    api_url: str = OLLAMA_API_URL,
) -> dict:
    request = Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Ollama screen vision endpoint returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError("Ollama screen vision endpoint could not be reached.") from exc
    except Exception as exc:
        raise RuntimeError("Ollama screen vision endpoint returned an invalid response.") from exc


def extract_screen_target_payload(response_text: str) -> dict:
    cleaned = response_text.strip()
    start_index = cleaned.find("{")
    end_index = cleaned.rfind("}")
    if start_index == -1 or end_index == -1:
        raise RuntimeError("Ollama did not return a JSON screen target payload.")
    return json.loads(cleaned[start_index : end_index + 1])


def locate_click_target_with_vision(
    target_name: str,
    target_description: str,
    encoded_image: str,
    model_name: str | None = None,
    request_sender=send_screen_target_request,
    tags_loader=list_installed_ollama_models,
) -> dict:
    installed_models = tags_loader()
    selected_model = model_name or select_best_available_ollama_model(
        installed_models,
        preferred_models=OLLAMA_SCREEN_VISION_MODEL_CANDIDATES,
    )
    payload = build_screen_target_payload(
        model_name=selected_model,
        target_name=target_name,
        target_description=target_description,
        encoded_image=encoded_image,
    )
    response_payload = request_sender(payload)
    response_text = extract_ollama_text(response_payload)
    if not response_text:
        raise RuntimeError(f"Ollama returned an empty screen target for model {selected_model}.")
    prediction = extract_screen_target_payload(response_text)
    found = bool(prediction.get("found", False))
    confidence = float(prediction.get("confidence", 0))
    x = int(prediction.get("x", 0))
    y = int(prediction.get("y", 0))
    reason = str(prediction.get("reason", "")).strip()
    return {
        "found": found and confidence >= SCREEN_VISION_MIN_CONFIDENCE and x >= 0 and y >= 0,
        "x": x,
        "y": y,
        "confidence": confidence,
        "reason": reason,
        "model_name": selected_model,
    }
