# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer el numero de resultados por defecto.
# 2. Embeddings: Para convertir consultas en vectores.
from config.chromadb_cheat_sheet_config import DEFAULT_N_RESULTS
from models.chromadb_keyword_embedding_gateway import build_keyword_embedding

# --- CONSULTAS ---
# 1.1. Funcion para leer todos los documentos de la coleccion.
def get_all_documents(collection):
    # Devuelve ids metadatos y documentos de la coleccion completa.
    return collection.get()


# 1.2. Funcion para recuperar documentos por id.
def get_documents_by_id(collection, ids: list[str]):
    # Devuelve ids metadatos y documentos del subconjunto pedido.
    return collection.get(ids=ids)


# 1.3. Funcion para filtrar por metadatos.
def get_documents_with_metadata_filter(collection, where_filter: dict):
    # Devuelve solo los elementos que cumplen el filtro indicado.
    return collection.get(where=where_filter)


# 1.4. Funcion para filtrar por contenido textual del documento.
def get_documents_with_document_filter(collection, where_document: dict):
    # Devuelve solo los documentos cuyo texto coincide con el filtro.
    return collection.get(where_document=where_document)


# 1.5. Funcion para ejecutar una consulta de similitud por embedding.
def query_by_text(
    collection,
    query_text: str,
    n_results: int = DEFAULT_N_RESULTS,
    where_filter: dict | None = None,
    where_document: dict | None = None,
):
    # Genera el embedding determinista de la consulta.
    query_embedding = build_keyword_embedding(query_text).tolist()

    # Ejecuta la consulta vectorial con filtros opcionales.
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_filter,
        where_document=where_document,
    )


# 1.6. Funcion para resumir resultados tipo get en texto legible.
def format_get_result(get_result: dict) -> str:
    # Extrae las listas principales del resultado.
    ids = get_result.get("ids", [])
    documents = get_result.get("documents", [])
    metadatas = get_result.get("metadatas", [])
    lines: list[str] = []

    # Recorre todos los elementos para presentarlos de forma compacta.
    for index, item_id in enumerate(ids):
        metadata = metadatas[index] if index < len(metadatas) else {}
        document = documents[index] if index < len(documents) else ""
        lines.append(f"{item_id} | {metadata} | {document}")

    # Devuelve un bloque legible o un aviso si no hubo datos.
    return "\n".join(lines) if lines else "Sin resultados."


# 1.7. Funcion para resumir resultados tipo query en texto legible.
def format_query_result(query_result: dict) -> str:
    # Extrae la primera lista de resultados de la consulta.
    ids = query_result.get("ids", [[]])[0]
    documents = query_result.get("documents", [[]])[0]
    distances = query_result.get("distances", [[]])[0]
    metadatas = query_result.get("metadatas", [[]])[0]
    lines: list[str] = []

    # Recorre cada vecino recuperado y lo muestra con su distancia.
    for index, item_id in enumerate(ids):
        distance = distances[index] if index < len(distances) else None
        metadata = metadatas[index] if index < len(metadatas) else {}
        document = documents[index] if index < len(documents) else ""
        lines.append(
            f"Rank {index + 1} | {item_id} | distance={distance} | {metadata} | {document}"
        )

    # Devuelve los vecinos recuperados o un aviso si no hubo match.
    return "\n".join(lines) if lines else "Sin resultados."
