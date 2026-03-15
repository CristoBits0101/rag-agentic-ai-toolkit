# --- DEPENDENCIAS ---
# 1. Math: Para la raiz cuadrada de la distancia euclidiana.
# 2. Numpy: Para operaciones vectoriales y matriciales.
import math

import numpy as np

# --- METRICAS ---
# 1.1. Funcion para calcular distancia euclidiana entre dos vectores.
def euclidean_distance_fn(vector1, vector2) -> float:
    # Suma diferencias al cuadrado y devuelve la raiz final.
    squared_sum = sum((x - y) ** 2 for x, y in zip(vector1, vector2))
    return math.sqrt(squared_sum)


# 1.2. Funcion para calcular toda la matriz L2 con doble bucle.
def build_l2_distance_matrix(embeddings: np.ndarray) -> np.ndarray:
    # Reserva una matriz cuadrada para todas las distancias.
    distance_matrix = np.zeros((embeddings.shape[0], embeddings.shape[0]))

    # Recorre todas las combinaciones posibles de vectores.
    for i in range(embeddings.shape[0]):
        for j in range(embeddings.shape[0]):
            distance_matrix[i, j] = euclidean_distance_fn(embeddings[i], embeddings[j])

    # Devuelve la matriz completa de distancias.
    return distance_matrix


# 1.3. Funcion para calcular L2 evitando trabajo redundante.
def build_l2_distance_matrix_improved(embeddings: np.ndarray) -> np.ndarray:
    # Reserva una matriz cuadrada inicializada a cero.
    distance_matrix = np.zeros((embeddings.shape[0], embeddings.shape[0]))

    # Recorre solo la mitad superior sin la diagonal.
    for i in range(embeddings.shape[0]):
        for j in range(i + 1, embeddings.shape[0]):
            distance = euclidean_distance_fn(embeddings[i], embeddings[j])
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance

    # Devuelve la matriz simetrica ya rellenada.
    return distance_matrix


# 1.4. Funcion para calcular L2 con Scipy si esta disponible.
def build_l2_distance_matrix_scipy(embeddings: np.ndarray) -> np.ndarray:
    # Importa Scipy solo cuando se solicita esta comparacion.
    try:
        from scipy.spatial.distance import cdist
    except ImportError as exc:
        raise ImportError("Falta scipy. Instala con pip install -U scipy.") from exc

    # Devuelve la matriz de distancias euclidianas.
    return cdist(embeddings, embeddings, "euclidean")


# 1.5. Funcion para calcular el producto punto entre dos vectores.
def dot_product_fn(vector1, vector2) -> float:
    # Multiplica componente a componente y suma el resultado.
    return sum(x * y for x, y in zip(vector1, vector2))


# 1.6. Funcion para calcular todos los productos punto con doble bucle.
def build_dot_product_matrix(embeddings: np.ndarray) -> np.ndarray:
    # Reserva una matriz cuadrada para todas las similitudes.
    similarity_matrix = np.empty((embeddings.shape[0], embeddings.shape[0]))

    # Recorre todas las parejas posibles de vectores.
    for i in range(embeddings.shape[0]):
        for j in range(embeddings.shape[0]):
            similarity_matrix[i, j] = dot_product_fn(embeddings[i], embeddings[j])

    # Devuelve la matriz completa de similitudes.
    return similarity_matrix


# 1.7. Funcion para calcular productos punto por algebra matricial.
def build_dot_product_matrix_operator(embeddings: np.ndarray) -> np.ndarray:
    # Multiplica la matriz por su transpuesta.
    return embeddings @ embeddings.T


# 1.8. Funcion para convertir similitud de producto punto en distancia.
def build_dot_product_distance_matrix(dot_product_matrix: np.ndarray) -> np.ndarray:
    # Niega la similitud para producir una distancia ordenable.
    return -dot_product_matrix


# 1.9. Funcion para calcular la norma L2 de cada embedding.
def calculate_l2_norms(embeddings: np.ndarray) -> np.ndarray:
    # Calcula la magnitud de cada fila del arreglo.
    return np.sqrt(np.sum(embeddings ** 2, axis=1))


# 1.10. Funcion para normalizar embeddings manualmente.
def normalize_embeddings_manual(embeddings: np.ndarray) -> np.ndarray:
    # Reorganiza normas para permitir broadcasting por fila.
    l2_norms = calculate_l2_norms(embeddings).reshape(-1, 1)

    # Devuelve embeddings con longitud unitaria.
    return embeddings / l2_norms


# 1.11. Funcion para verificar que todos los vectores normalizados miden uno.
def verify_normalized_embeddings(normalized_embeddings: np.ndarray) -> np.ndarray:
    # Recalcula normas para validar la normalizacion.
    return calculate_l2_norms(normalized_embeddings)


# 1.12. Funcion para normalizar embeddings con Torch si esta disponible.
def normalize_embeddings_torch(embeddings: np.ndarray) -> np.ndarray:
    # Importa Torch solo cuando se solicita esta comparacion.
    try:
        import torch
    except ImportError as exc:
        raise ImportError("Falta torch. Instala con pip install -U torch.") from exc

    # Devuelve embeddings normalizados desde Torch en formato Numpy.
    return torch.nn.functional.normalize(torch.from_numpy(embeddings)).numpy()


# 1.13. Funcion para calcular similitud coseno con doble bucle.
def build_cosine_similarity_matrix(normalized_embeddings: np.ndarray) -> np.ndarray:
    # Reserva una matriz cuadrada para todas las similitudes.
    similarity_matrix = np.empty(
        (normalized_embeddings.shape[0], normalized_embeddings.shape[0])
    )

    # Recorre todas las parejas de embeddings ya normalizados.
    for i in range(normalized_embeddings.shape[0]):
        for j in range(normalized_embeddings.shape[0]):
            similarity_matrix[i, j] = dot_product_fn(
                normalized_embeddings[i],
                normalized_embeddings[j],
            )

    # Devuelve la matriz completa de cosenos.
    return similarity_matrix


# 1.14. Funcion para calcular similitud coseno por algebra matricial.
def build_cosine_similarity_matrix_operator(
    normalized_embeddings: np.ndarray,
) -> np.ndarray:
    # Multiplica embeddings normalizados por su transpuesta.
    return normalized_embeddings @ normalized_embeddings.T


# 1.15. Funcion para convertir similitud coseno en distancia coseno.
def build_cosine_distance_matrix(cosine_similarity_matrix: np.ndarray) -> np.ndarray:
    # Resta la similitud a uno para obtener distancia.
    return 1 - cosine_similarity_matrix
