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
from config.chromadb_cheat_sheet_config import CRUD_DEMO_ID
from config.chromadb_cheat_sheet_config import HNSW_SPACE
from data.chromadb_demo_dataset import CRUD_DEMO_ITEM
from data.chromadb_demo_dataset import DEMO_ITEMS
from models.chromadb_keyword_embedding_gateway import build_keyword_embedding
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


# 1.3. Funcion para conectarse a una coleccion ya creada.
def get_existing_collection():
    # Obtiene el cliente local de la practica.
    client = get_client()
    collection = client.get_collection(COLLECTION_NAME)
    runtime_state.collection = collection
    runtime_state.collection_name = COLLECTION_NAME

    # Devuelve la coleccion ya registrada.
    return collection


# 1.4. Funcion para cargar el dataset de ejemplo en la coleccion.
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


# 1.5. Funcion para actualizar metadatos de la coleccion.
def modify_collection_metadata(collection, metadata: dict):
    # Aplica nuevos metadatos sobre la coleccion actual.
    collection.modify(metadata=metadata)

    # Devuelve la coleccion con metadatos actualizados.
    return collection


# 1.6. Funcion para insertar un documento CRUD de demostracion.
def add_crud_demo_item(collection):
    # Inserta un documento adicional con embedding determinista.
    collection.add(
        ids=[CRUD_DEMO_ITEM["id"]],
        documents=[CRUD_DEMO_ITEM["document"]],
        metadatas=[CRUD_DEMO_ITEM["metadata"]],
        embeddings=[build_keyword_embedding(CRUD_DEMO_ITEM["document"]).tolist()],
    )

    # Devuelve la coleccion tras la insercion.
    return collection


# 1.7. Funcion para actualizar el documento CRUD de demostracion.
def update_crud_demo_item(collection):
    # Define el nuevo contenido para el documento de prueba.
    updated_document = (
        "Recommendation systems and RAG pipelines reuse vector retrieval to rank similar content."
    )
    updated_metadata = {
        "topic": "recommendation",
        "source": "product.blog",
        "version": 2.0,
    }
    collection.update(
        ids=[CRUD_DEMO_ID],
        documents=[updated_document],
        metadatas=[updated_metadata],
        embeddings=[build_keyword_embedding(updated_document).tolist()],
    )

    # Devuelve el contenido actualizado para facilitar la validacion.
    return updated_document, updated_metadata


# 1.8. Funcion para eliminar el documento CRUD de demostracion.
def delete_crud_demo_item(collection):
    # Elimina el documento agregado para la demo.
    collection.delete(ids=[CRUD_DEMO_ID])

    # Devuelve la coleccion tras la eliminacion.
    return collection


# 1.9. Funcion para construir y poblar una coleccion lista para consultas.
def bootstrap_demo_collection():
    # Crea una coleccion limpia para la ejecucion actual.
    collection = create_demo_collection()

    # Inserta los documentos de ejemplo con embeddings deterministas.
    return seed_demo_collection(collection)
