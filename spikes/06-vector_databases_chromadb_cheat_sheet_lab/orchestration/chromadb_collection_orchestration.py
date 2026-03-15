# --- DEPENDENCIAS ---
# 1. ChromaDB: Para crear cliente y colecciones locales.
# 2. Settings: Para inicializar un cliente en memoria.
# 3. Configuracion: Para leer nombre de coleccion y espacio HNSW.
# 4. Datos: Para cargar el corpus de ejemplo.
# 5. Embeddings: Para generar vectores sin modelos externos.
# 6. Estado: Para reutilizar cliente y coleccion.
import chromadb
from chromadb.config import Settings

from config.chromadb_cheat_sheet_config import COLLECTION_NAME
from config.chromadb_cheat_sheet_config import HNSW_SPACE
from data.chromadb_demo_dataset import DEMO_ITEMS
from models.chromadb_keyword_embedding_gateway import build_keyword_embeddings
from state.chromadb_runtime_state import runtime_state

# --- COLECCION ---
# 1.1. Funcion para crear un cliente local en memoria.
def get_client():
    # Reutiliza el cliente si ya fue inicializado antes.
    if runtime_state.client is None:
        runtime_state.client = chromadb.Client(
            Settings(
                is_persistent=False,
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )

    # Devuelve el cliente listo para usar.
    return runtime_state.client


# 1.2. Funcion para crear una coleccion limpia de demostracion.
def create_demo_collection():
    # Obtiene el cliente local de la practica.
    client = get_client()

    # Elimina la coleccion previa si existe para asegurar un estado limpio.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    # Crea una coleccion nueva con HNSW y distancia coseno.
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"topic": "query testing"},
        configuration={"hnsw": {"space": HNSW_SPACE}},
    )
    runtime_state.collection = collection
    runtime_state.collection_name = COLLECTION_NAME

    # Devuelve la coleccion lista para poblar.
    return collection


# 1.3. Funcion para cargar el dataset de ejemplo en la coleccion.
def seed_demo_collection(collection):
    # Extrae ids documentos y metadatos del dataset base.
    ids = [item["id"] for item in DEMO_ITEMS]
    documents = [item["document"] for item in DEMO_ITEMS]
    metadatas = [item["metadata"] for item in DEMO_ITEMS]
    embeddings = build_keyword_embeddings(documents)
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    # Devuelve la coleccion ya poblada.
    return collection


# 1.4. Funcion para construir y poblar una coleccion lista para consultas.
def bootstrap_demo_collection():
    # Crea una coleccion limpia para la ejecucion actual.
    collection = create_demo_collection()

    # Inserta los documentos de ejemplo con embeddings deterministas.
    return seed_demo_collection(collection)
