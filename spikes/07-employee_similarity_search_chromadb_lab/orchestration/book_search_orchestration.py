# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer el numero de resultados por defecto.
# 2. Embeddings: Para convertir consultas en vectores.
from config.employee_similarity_config import DEFAULT_N_RESULTS
from models.employee_book_embedding_gateway import build_book_embedding

# --- CONSULTAS ---
# 1.1. Funcion para recuperar libros por similitud.
def query_books(
    collection,
    query_text: str,
    n_results: int = DEFAULT_N_RESULTS,
    where_filter: dict | None = None,
):
    # Genera el embedding de la consulta del usuario.
    query_embedding = build_book_embedding(query_text).tolist()

    # Ejecuta la consulta vectorial con filtros opcionales.
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_filter,
    )


# 1.2. Funcion para recuperar libros por filtro exacto.
def get_books(collection, where_filter: dict):
    # Devuelve solo los documentos que cumplen el filtro.
    return collection.get(where=where_filter)


# 1.3. Funcion para buscar aventuras magicas de fantasia.
def search_magical_fantasy_adventures(collection):
    # Ejecuta la consulta semantica del ejercicio.
    return query_books(
        collection,
        "magical fantasy adventure with friendship and courage",
    )


# 1.4. Funcion para filtrar libros de fantasia y ciencia ficcion.
def get_fantasy_and_science_fiction_books(collection):
    # Filtra por generos incluidos.
    return get_books(
        collection,
        {"genre": {"$in": ["Fantasy", "Science Fiction"]}},
    )


# 1.5. Funcion para filtrar libros con rating alto.
def get_highly_rated_books(collection):
    # Filtra por rating de cuatro punto tres o mayor.
    return get_books(collection, {"rating": {"$gte": 4.3}})


# 1.6. Funcion para combinar similitud y rating.
def search_highly_rated_dystopian_books(collection):
    # Busca temas distopicos con restriccion de rating alto.
    return query_books(
        collection,
        "dystopian society control oppression future",
        n_results=3,
        where_filter={"rating": {"$gte": 4.0}},
    )
