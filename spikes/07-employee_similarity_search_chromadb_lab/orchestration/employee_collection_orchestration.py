# --- DEPENDENCIAS ---
# 1. ChromaDB: Para crear cliente y colecciones locales.
# 2. Settings: Para inicializar un cliente en memoria.
# 3. Configuracion: Para leer nombre de coleccion y distancia.
# 4. Datos: Para cargar el dataset de empleados.
# 5. Embeddings: Para generar vectores locales.
# 6. Estado: Para reutilizar cliente y coleccion.
import chromadb
from chromadb.config import Settings

from config.employee_similarity_config import EMPLOYEE_COLLECTION_NAME
from config.employee_similarity_config import HNSW_SPACE
from data.employee_records import EMPLOYEES
from models.employee_book_embedding_gateway import build_employee_embeddings
from state.employee_similarity_state import runtime_state

# --- COLECCION ---
# 1.1. Funcion para crear o reutilizar un cliente local en memoria.
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


# 1.2. Funcion para construir documentos enriquecidos de empleados.
def build_employee_documents() -> list[str]:
    # Acumula un documento descriptivo por empleado.
    documents: list[str] = []

    # Combina rol experiencia departamento habilidades y ubicacion.
    for employee in EMPLOYEES:
        document = (
            f"{employee['role']} with {employee['experience']} years of experience in "
            f"{employee['department']}. Skills: {employee['skills']}. Located in "
            f"{employee['location']}. Employment type: {employee['employment_type']}."
        )
        documents.append(document)

    # Devuelve los documentos listos para embedding.
    return documents


# 1.3. Funcion para crear una coleccion limpia de empleados.
def create_employee_collection():
    # Obtiene el cliente local del spike.
    client = get_client()

    # Elimina la coleccion previa si existe para asegurar estado limpio.
    try:
        client.delete_collection(EMPLOYEE_COLLECTION_NAME)
    except Exception:
        pass

    # Crea una coleccion nueva con HNSW y distancia coseno.
    collection = client.create_collection(
        name=EMPLOYEE_COLLECTION_NAME,
        metadata={"description": "A collection for storing employee data"},
        configuration={"hnsw": {"space": HNSW_SPACE}},
    )
    runtime_state.employee_collection = collection

    # Devuelve la coleccion lista para poblar.
    return collection


# 1.4. Funcion para cargar el dataset de empleados en la coleccion.
def seed_employee_collection(collection):
    # Construye documentos y embeddings del dataset.
    documents = build_employee_documents()
    embeddings = build_employee_embeddings(documents)
    collection.add(
        ids=[employee["id"] for employee in EMPLOYEES],
        documents=documents,
        metadatas=[
            {
                "name": employee["name"],
                "department": employee["department"],
                "role": employee["role"],
                "experience": employee["experience"],
                "location": employee["location"],
                "employment_type": employee["employment_type"],
            }
            for employee in EMPLOYEES
        ],
        embeddings=embeddings,
    )

    # Devuelve la coleccion ya poblada.
    return collection


# 1.5. Funcion para crear y poblar la coleccion de empleados.
def bootstrap_employee_collection():
    # Crea una coleccion nueva para la ejecucion actual.
    collection = create_employee_collection()

    # Inserta documentos metadatos y embeddings deterministas.
    return seed_employee_collection(collection)
