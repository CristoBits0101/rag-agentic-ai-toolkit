# --- DEPENDENCIAS ---
# 1. Dataclass: Para agrupar el estado en memoria.
# 2.       Any: Para describir dependencias cargadas en tiempo de ejecucion.
from dataclasses import dataclass
from typing import Any

# --- ESTADO ---
# 1.1. Modelo de datos para el estado del spike.
@dataclass
class RagRuntimeState:
    # Guarda el modelo de lenguaje ya cargado.
    llm_model: Any = None
    # Guarda el modelo de embeddings ya cargado.
    embedding_model: Any = None
    # Guarda la ruta del PDF ya indexado.
    indexed_pdf_path: str | None = None
    # Guarda la base vectorial ya creada.
    vector_store: Any = None
    # Guarda el retriever ya creado.
    rag_retriever: Any = None


# 1.2. Instancia compartida para reutilizar estado en memoria.
runtime_state = RagRuntimeState()
