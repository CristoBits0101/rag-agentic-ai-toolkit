# --- DEPENDENCIAS ---
# 1. ChromaDB: Para crear cliente y coleccion local.
# 2. Settings: Para inicializar un cliente en memoria.
# 3. Configuracion: Para leer nombre de coleccion y distancia.
# 4. Embeddings: Para generar vectores deterministas.
# 5. Pipeline: Para cargar documentos y metadatos del dataset.
# 6. Estado: Para reutilizar cliente y coleccion.
import chromadb
from chromadb.config import Settings

from config.food_recommendation_config import COLLECTION_NAME
from config.food_recommendation_config import HNSW_SPACE
from models.food_embedding_gateway import build_food_embeddings
from pipeline.food_data_pipeline import build_food_document
from pipeline.food_data_pipeline import build_food_metadata
from pipeline.food_data_pipeline import load_food_data
from state.food_recommendation_state import runtime_state

# --- COLECCION ---
# 1.1. Funcion para crear o reutilizar un cliente local.
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


# 1.2. Funcion para crear una coleccion limpia de recomendaciones.
def create_food_collection():
    # Obtiene el cliente local del spike.
    client = get_client()

    # Elimina la coleccion previa si existe para asegurar estado limpio.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    # Crea la coleccion con distancia coseno.
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "A collection for food recommendation systems"},
        configuration={"hnsw": {"space": HNSW_SPACE}},
    )
    runtime_state.collection = collection

    # Devuelve la coleccion vacia.
    return collection


# 1.3. Funcion para poblar la coleccion con el dataset local.
def seed_food_collection(collection):
    # Carga y transforma el dataset del dominio.
    food_items = load_food_data()
    documents = [build_food_document(food_item) for food_item in food_items]
    metadatas = [build_food_metadata(food_item) for food_item in food_items]
    embeddings = build_food_embeddings(documents)
    ids = [food_item["food_id"] for food_item in food_items]
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    # Devuelve la coleccion y el dataset ya cargado.
    return collection, food_items


# 1.4. Funcion para crear y poblar la coleccion principal.
def bootstrap_food_collection():
    # Crea una coleccion nueva para la ejecucion actual.
    collection = create_food_collection()

    # Inserta documentos metadatos y embeddings locales.
    return seed_food_collection(collection)
