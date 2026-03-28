# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer filtros reutilizables del dominio.
# 2. Embeddings: Para convertir consultas en vectores.
from config.employee_similarity_config import CALIFORNIA_LOCATIONS
from config.employee_similarity_config import DEFAULT_N_RESULTS
from config.employee_similarity_config import EMPLOYEE_MAJOR_TECH_CITIES
from models.employee_book_embedding_gateway import build_employee_embedding

# --- CONSULTAS ---
# 1.1. Funcion para recuperar empleados por similitud.
def query_employees(
    collection,
    query_text: str,
    n_results: int = DEFAULT_N_RESULTS,
    where_filter: dict | None = None,
):
    # Genera el embedding de la consulta del usuario.
    query_embedding = build_employee_embedding(query_text).tolist()

    # Ejecuta la consulta vectorial con filtros opcionales.
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_filter,
    )


# 1.2. Funcion para recuperar empleados por filtro exacto.
def get_employees(collection, where_filter: dict):
    # Devuelve solo los documentos que cumplen el filtro.
    return collection.get(where=where_filter)


# 1.3. Funcion para buscar desarrolladores Python.
def search_python_developers(collection):
    # Ejecuta la consulta semantica principal del laboratorio.
    return query_employees(
        collection,
        "Python developer with web development experience",
    )


# 1.4. Funcion para buscar roles de liderazgo.
def search_leadership_roles(collection):
    # Ejecuta la consulta de liderazgo y gestion.
    return query_employees(
        collection,
        "team leader manager with experience",
    )


# 1.5. Funcion para listar empleados de ingenieria.
def get_engineering_employees(collection):
    # Filtra por departamento exacto.
    return get_employees(collection, {"department": "Engineering"})


# 1.6. Funcion para listar empleados con diez o mas anos.
def get_senior_employees(collection):
    # Filtra por rango de experiencia minima.
    return get_employees(collection, {"experience": {"$gte": 10}})


# 1.7. Funcion para listar empleados de California.
def get_california_employees(collection):
    # Filtra por ciudades de California usadas en la practica.
    return get_employees(collection, {"location": {"$in": CALIFORNIA_LOCATIONS}})


# 1.8. Funcion para combinar similitud y metadatos.
def search_senior_python_developers_in_tech_cities(collection):
    # Busca perfiles senior en ciudades tecnicas clave.
    return query_employees(
        collection,
        "senior Python developer full-stack",
        n_results=5,
        where_filter={
            "$and": [
                {"experience": {"$gte": 8}},
                {"location": {"$in": EMPLOYEE_MAJOR_TECH_CITIES}},
            ]
        },
    )


# 1.9. Funcion para provocar un caso sin resultados.
def search_empty_employee_case(collection):
    # Ejecuta una combinacion imposible para verificar el manejo de vacios.
    return query_employees(
        collection,
        "part time senior HR executive in Seattle",
        n_results=3,
        where_filter={
            "$and": [
                {"employment_type": "Part-time"},
                {"experience": {"$gte": 15}},
                {"location": "Seattle"},
            ]
        },
    )
