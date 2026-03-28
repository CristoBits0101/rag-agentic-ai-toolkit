# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer nombre de coleccion y distancia.
# 2. Datos: Para cargar el dataset de libros.
# 3. Embeddings: Para generar vectores locales.
# 4. Coleccion Empleados: Para reutilizar el mismo cliente.
# 5. Estado: Para reutilizar la coleccion de libros.
from config.employee_similarity_config import BOOK_COLLECTION_NAME
from config.employee_similarity_config import HNSW_SPACE
from data.book_records import BOOKS
from models.employee_book_embedding_gateway import build_book_embeddings
from orchestration.employee_collection_orchestration import get_client
from state.employee_similarity_state import runtime_state

# --- COLECCION ---
# 1.1. Funcion para construir documentos enriquecidos de libros.
def build_book_documents() -> list[str]:
    # Acumula un documento descriptivo por libro.
    documents: list[str] = []

    # Combina titulo descripcion temas y ambientacion.
    for book in BOOKS:
        document = (
            f"{book['title']} by {book['author']}. {book['description']} "
            f"Themes: {book['themes']}. Setting: {book['setting']}. "
            f"Genre: {book['genre']} published in {book['year']}."
        )
        documents.append(document)

    # Devuelve los documentos listos para embedding.
    return documents


# 1.2. Funcion para crear una coleccion limpia de libros.
def create_book_collection():
    # Reutiliza el cliente local del spike.
    client = get_client()

    # Elimina la coleccion previa si existe para asegurar estado limpio.
    try:
        client.delete_collection(BOOK_COLLECTION_NAME)
    except Exception:
        pass

    # Crea una coleccion nueva con HNSW y distancia coseno.
    collection = client.create_collection(
        name=BOOK_COLLECTION_NAME,
        metadata={"description": "A collection for storing book data"},
        configuration={"hnsw": {"space": HNSW_SPACE}},
    )
    runtime_state.book_collection = collection

    # Devuelve la coleccion lista para poblar.
    return collection


# 1.3. Funcion para cargar el dataset de libros en la coleccion.
def seed_book_collection(collection):
    # Construye documentos y embeddings del dataset.
    documents = build_book_documents()
    embeddings = build_book_embeddings(documents)
    collection.add(
        ids=[book["id"] for book in BOOKS],
        documents=documents,
        metadatas=[
            {
                "title": book["title"],
                "author": book["author"],
                "genre": book["genre"],
                "year": book["year"],
                "rating": book["rating"],
                "pages": book["pages"],
            }
            for book in BOOKS
        ],
        embeddings=embeddings,
    )

    # Devuelve la coleccion ya poblada.
    return collection


# 1.4. Funcion para crear y poblar la coleccion de libros.
def bootstrap_book_collection():
    # Crea una coleccion nueva para la ejecucion actual.
    collection = create_book_collection()

    # Inserta documentos metadatos y embeddings deterministas.
    return seed_book_collection(collection)
