# --- DEPENDENCIAS ---
# 1. Colecciones Libros: Para cargar la coleccion del ejercicio.
# 2. Colecciones Empleados: Para cargar la coleccion principal.
# 3. Busqueda Libros: Para ejecutar consultas y filtros del ejercicio.
# 4. Busqueda Empleados: Para ejecutar consultas y filtros del laboratorio.
from orchestration.book_collection_orchestration import bootstrap_book_collection
from orchestration.book_search_orchestration import get_fantasy_and_science_fiction_books
from orchestration.book_search_orchestration import get_highly_rated_books
from orchestration.book_search_orchestration import search_highly_rated_dystopian_books
from orchestration.book_search_orchestration import search_magical_fantasy_adventures
from orchestration.employee_collection_orchestration import bootstrap_employee_collection
from orchestration.employee_search_orchestration import get_california_employees
from orchestration.employee_search_orchestration import get_engineering_employees
from orchestration.employee_search_orchestration import get_senior_employees
from orchestration.employee_search_orchestration import search_empty_employee_case
from orchestration.employee_search_orchestration import search_leadership_roles
from orchestration.employee_search_orchestration import search_python_developers
from orchestration.employee_search_orchestration import (
    search_senior_python_developers_in_tech_cities,
)

# --- RUNNER ---
# 1.1. Funcion para imprimir encabezados de seccion.
def print_section(title: str):
    # Separa visualmente cada bloque de resultados.
    print(f"\n=== {title} ===")


# 1.2. Funcion para imprimir resultados de similitud.
def print_query_results(results, label_fields: list[str]):
    # Sale temprano si la consulta no devuelve vecinos.
    if not results or not results["ids"] or len(results["ids"][0]) == 0:
        print("No documents found for the query.")
        return

    # Recorre los vecinos recuperados y muestra su resumen.
    for index, item_id in enumerate(results["ids"][0]):
        metadata = results["metadatas"][0][index]
        distance = results["distances"][0][index]
        fields = " | ".join(str(metadata[field]) for field in label_fields)
        print(f"  {index + 1}. {item_id} | {fields} | Distance: {distance:.4f}")


# 1.3. Funcion para imprimir resultados de filtros exactos.
def print_get_results(results, label_fields: list[str]):
    # Recorre los elementos del get y muestra un resumen corto.
    for index, item_id in enumerate(results["ids"]):
        metadata = results["metadatas"][index]
        fields = " | ".join(str(metadata[field]) for field in label_fields)
        print(f"  - {item_id} | {fields}")


# 1.4. Funcion para ejecutar la practica completa.
def run_employee_similarity_lab():
    # Crea y carga la coleccion principal de empleados.
    employee_collection = bootstrap_employee_collection()
    employee_items = employee_collection.get()
    print("Collection created: employee_collection")
    print("Collection contents:")
    print(f"Number of documents: {len(employee_items['documents'])}")

    print_section("Similarity Search Examples")
    print("1. Searching for Python developers.")
    print_query_results(
        search_python_developers(employee_collection),
        ["name", "role", "department"],
    )
    print("\n2. Searching for leadership and management roles.")
    print_query_results(
        search_leadership_roles(employee_collection),
        ["name", "role", "experience"],
    )

    print_section("Metadata Filtering Examples")
    print("3. Finding all Engineering employees.")
    print_get_results(
        get_engineering_employees(employee_collection),
        ["name", "role", "experience"],
    )
    print("\n4. Finding employees with 10 plus years experience.")
    print_get_results(
        get_senior_employees(employee_collection),
        ["name", "role", "experience"],
    )
    print("\n5. Finding employees in California.")
    print_get_results(
        get_california_employees(employee_collection),
        ["name", "location"],
    )

    print_section("Combined Search")
    print("6. Finding senior Python developers in major tech cities.")
    print_query_results(
        search_senior_python_developers_in_tech_cities(employee_collection),
        ["name", "role", "location", "experience"],
    )
    print("\n7. Checking an empty result case.")
    print_query_results(
        search_empty_employee_case(employee_collection),
        ["name", "role"],
    )

    # Crea y carga la coleccion secundaria de libros.
    book_collection = bootstrap_book_collection()
    book_items = book_collection.get()
    print_section("Book Practice Exercise")
    print("Collection created: book_collection")
    print(f"Number of documents: {len(book_items['documents'])}")
    print("\n1. Finding magical fantasy adventures.")
    print_query_results(
        search_magical_fantasy_adventures(book_collection),
        ["title", "author", "genre"],
    )
    print("\n2. Finding Fantasy and Science Fiction books.")
    print_get_results(
        get_fantasy_and_science_fiction_books(book_collection),
        ["title", "genre", "rating"],
    )
    print("\n3. Finding highly rated books.")
    print_get_results(
        get_highly_rated_books(book_collection),
        ["title", "rating"],
    )
    print("\n4. Finding highly rated dystopian books.")
    print_query_results(
        search_highly_rated_dystopian_books(book_collection),
        ["title", "year", "rating"],
    )
