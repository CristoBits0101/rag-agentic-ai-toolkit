# --- DEPENDENCIAS ---
# 1. Regex: Para tokenizar texto de forma simple.
# 2. Numpy: Para devolver embeddings listos para ChromaDB.
import re

import numpy as np

# --- EMBEDDINGS ---
# 1.1. Grupos de palabras clave para empleados.
EMPLOYEE_KEYWORD_GROUPS = {
    "engineering": {
        "architect",
        "backend",
        "cloud",
        "databases",
        "devops",
        "developer",
        "engineering",
        "engineer",
        "frontend",
        "full",
        "microservices",
        "node",
        "python",
        "react",
        "software",
        "stack",
        "web",
    },
    "python_web": {
        "css",
        "development",
        "developer",
        "full",
        "html",
        "javascript",
        "node",
        "python",
        "react",
        "stack",
        "web",
    },
    "python_specific": {
        "python",
    },
    "leadership": {
        "architect",
        "director",
        "lead",
        "leader",
        "leadership",
        "manager",
        "mentoring",
        "principal",
        "project",
        "senior",
        "strategy",
        "team",
    },
    "hr": {
        "compensation",
        "conflict",
        "employee",
        "engagement",
        "hr",
        "organizational",
        "performance",
        "policies",
        "recruitment",
        "relations",
        "training",
    },
    "marketing": {
        "advertising",
        "analytics",
        "brand",
        "campaign",
        "content",
        "creative",
        "digital",
        "email",
        "marketing",
        "research",
        "seo",
        "social",
        "strategy",
    },
    "cloud_devops": {
        "architecture",
        "automation",
        "aws",
        "cd",
        "ci",
        "cloud",
        "devops",
        "docker",
        "infrastructure",
        "kubernetes",
        "microservices",
        "pipelines",
        "spring",
    },
    "data_ml": {
        "analytics",
        "data",
        "learning",
        "machine",
        "science",
    },
    "tech_city": {
        "francisco",
        "new",
        "san",
        "seattle",
        "york",
    },
    "california": {
        "angeles",
        "francisco",
        "los",
        "san",
    },
    "full_time": {
        "full",
        "time",
    },
    "part_time": {
        "part",
        "time",
    },
}
BOOK_KEYWORD_GROUPS = {
    "fantasy_magic": {
        "adventure",
        "courage",
        "fantasy",
        "friendship",
        "hogwarts",
        "magic",
        "magical",
        "quest",
        "ring",
        "wizard",
    },
    "science_fiction": {
        "arrakis",
        "future",
        "galaxy",
        "planet",
        "science",
        "space",
        "technology",
    },
    "dystopian": {
        "control",
        "dystopian",
        "future",
        "oppression",
        "rebellion",
        "society",
        "surveillance",
        "survival",
        "totalitarian",
    },
    "authoritarian_dystopia": {
        "control",
        "freedom",
        "surveillance",
        "totalitarian",
        "truth",
    },
    "classic": {
        "american",
        "classic",
        "dream",
        "injustice",
        "jazz",
        "moral",
        "racism",
        "social",
        "wealth",
    },
    "power_politics": {
        "corruption",
        "ecology",
        "heroism",
        "politics",
        "power",
        "religion",
    },
}


# 1.2. Funcion para tokenizar texto de entrada.
def tokenize_text(text: str) -> list[str]:
    # Convierte a minusculas y extrae solo palabras simples.
    return re.findall(r"[a-z0-9]+", text.lower())


# 1.3. Funcion para crear un embedding de empleados.
def build_employee_embedding(text: str) -> np.ndarray:
    # Tokeniza el texto antes de contar dominios semanticos.
    tokens = tokenize_text(text)
    python_specific_score = float(
        sum(token in EMPLOYEE_KEYWORD_GROUPS["python_specific"] for token in tokens)
    )
    vector = np.array(
        [
            float(sum(token in EMPLOYEE_KEYWORD_GROUPS["engineering"] for token in tokens)),
            float(sum(token in EMPLOYEE_KEYWORD_GROUPS["python_web"] for token in tokens)),
            python_specific_score * 4.0,
            float(sum(token in EMPLOYEE_KEYWORD_GROUPS["leadership"] for token in tokens)),
            float(sum(token in EMPLOYEE_KEYWORD_GROUPS["hr"] for token in tokens)),
            float(sum(token in EMPLOYEE_KEYWORD_GROUPS["marketing"] for token in tokens)),
            float(sum(token in EMPLOYEE_KEYWORD_GROUPS["cloud_devops"] for token in tokens)),
            float(sum(token in EMPLOYEE_KEYWORD_GROUPS["data_ml"] for token in tokens)),
            float(sum(token in EMPLOYEE_KEYWORD_GROUPS["tech_city"] for token in tokens)),
            float(sum(token in EMPLOYEE_KEYWORD_GROUPS["california"] for token in tokens)),
            float(sum(token in EMPLOYEE_KEYWORD_GROUPS["full_time"] for token in tokens)),
            float(sum(token in EMPLOYEE_KEYWORD_GROUPS["part_time"] for token in tokens)),
        ],
        dtype=np.float32,
    )

    # Evita vectores nulos para no degradar la similitud coseno.
    if not vector.any():
        return np.ones(12, dtype=np.float32)

    # Devuelve el embedding como vector Numpy.
    return vector


# 1.4. Funcion para crear embeddings para empleados.
def build_employee_embeddings(texts: list[str]) -> list[list[float]]:
    # Devuelve cada embedding en formato serializable para ChromaDB.
    return [build_employee_embedding(text).tolist() for text in texts]


# 1.5. Funcion para crear un embedding de libros.
def build_book_embedding(text: str) -> np.ndarray:
    # Tokeniza el texto antes de contar dominios semanticos.
    tokens = tokenize_text(text)
    authoritarian_score = float(
        sum(token in BOOK_KEYWORD_GROUPS["authoritarian_dystopia"] for token in tokens)
    )
    vector = np.array(
        [
            float(sum(token in BOOK_KEYWORD_GROUPS["fantasy_magic"] for token in tokens)),
            float(sum(token in BOOK_KEYWORD_GROUPS["science_fiction"] for token in tokens)),
            float(sum(token in BOOK_KEYWORD_GROUPS["dystopian"] for token in tokens)),
            authoritarian_score * 4.0,
            float(sum(token in BOOK_KEYWORD_GROUPS["classic"] for token in tokens)),
            float(sum(token in BOOK_KEYWORD_GROUPS["power_politics"] for token in tokens)),
        ],
        dtype=np.float32,
    )

    # Evita vectores nulos para no degradar la similitud coseno.
    if not vector.any():
        return np.ones(6, dtype=np.float32)

    # Devuelve el embedding como vector Numpy.
    return vector


# 1.6. Funcion para crear embeddings para libros.
def build_book_embeddings(texts: list[str]) -> list[list[float]]:
    # Devuelve cada embedding en formato serializable para ChromaDB.
    return [build_book_embedding(text).tolist() for text in texts]
