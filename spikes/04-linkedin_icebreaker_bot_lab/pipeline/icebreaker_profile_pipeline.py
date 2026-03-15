# --- DEPENDENCIAS ---
# 1. JSON: Para leer perfiles mock desde disco.
# 2. TextSplitter: Para dividir el perfil en trozos.
# 3. Document: Para representar el texto del perfil.
# 4. Configuracion: Para leer rutas y tamano de chunk.
import json

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config.icebreaker_config import CHUNK_OVERLAP
from config.icebreaker_config import CHUNK_SIZE
from config.icebreaker_config import PROFILE_DATA_DIR

# --- PIPELINE ---
# 1.1. Funcion para listar las claves de perfiles mock disponibles.
def list_profile_keys() -> list[str]:
    # Devuelve los nombres de archivo sin extension y en orden alfabetico.
    return [file_path.stem for file_path in sorted(PROFILE_DATA_DIR.glob("*.json"))]


# 1.2. Funcion para cargar el JSON de un perfil mock.
def load_profile_data(profile_key: str) -> dict:
    # Resuelve la ruta del perfil usando su clave publica.
    profile_path = PROFILE_DATA_DIR / f"{profile_key}.json"

    # Frena la ejecucion si el perfil no existe en disco.
    if not profile_path.exists():
        raise FileNotFoundError(f"Perfil no encontrado: {profile_key}")

    # Lee y devuelve el contenido JSON del perfil.
    with profile_path.open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


# 1.3. Funcion para construir una etiqueta corta del perfil.
def build_profile_label(profile_data: dict) -> str:
    # Usa nombre y titular para mostrar el perfil en la interfaz.
    return f"{profile_data.get('full_name', 'Perfil')} - {profile_data.get('headline', 'Sin headline')}"


# 1.4. Funcion para construir las opciones visibles del selector.
def list_profile_choices() -> list[tuple[str, str]]:
    # Convierte cada perfil en una pareja etiqueta valor para Gradio.
    return [
        (build_profile_label(load_profile_data(profile_key)), profile_key)
        for profile_key in list_profile_keys()
    ]


# 1.5. Funcion para convertir el JSON en texto plano legible por el modelo.
def format_profile_text(profile_data: dict) -> str:
    # Acumula las lineas normalizadas del perfil.
    lines: list[str] = []

    # Recorre estructuras anidadas para convertirlas en pares clave valor.
    def append_lines(prefix: str, value):
        # Expande diccionarios manteniendo un orden estable.
        if isinstance(value, dict):
            for key in sorted(value):
                nested_prefix = f"{prefix}.{key}" if prefix else key
                append_lines(nested_prefix, value[key])
            return

        # Expande listas usando indices legibles.
        if isinstance(value, list):
            for index, item in enumerate(value, start=1):
                nested_prefix = f"{prefix}.{index}" if prefix else str(index)
                append_lines(nested_prefix, item)
            return

        # Descarta valores vacios para mejorar el contexto final.
        if value in ("", None):
            return

        # Guarda la linea final en formato simple.
        lines.append(f"{prefix}: {value}")

    # Ejecuta la conversion desde la raiz del perfil.
    append_lines("", profile_data)

    # Devuelve el perfil como bloque de texto continuo.
    return "\n".join(lines)


# 1.6. Funcion para partir el perfil en trozos listos para retrieval.
def prepare_profile_chunks(profile_key: str):
    # Carga el perfil seleccionado y lo transforma a texto plano.
    profile_data = load_profile_data(profile_key)
    profile_text = format_profile_text(profile_data)
    document = Document(
        page_content=profile_text,
        metadata={"profile_key": profile_key},
    )
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    # Devuelve los trozos listos para embeddings y retrieval.
    return splitter.split_documents([document])
