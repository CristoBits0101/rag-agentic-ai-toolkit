# --- DEPENDENCIAS ---
# 1. Dataclass: Para definir el estado compartido del spike.
# 2. Any: Para tipar recursos externos sin acoplar el modulo.
from dataclasses import dataclass
from typing import Any

# --- ESTADO ---
# 1.1. Clase que centraliza recursos reutilizables del laboratorio.
@dataclass
class SimilarityRuntimeState:
    model_name: str = ""
    embedding_model: Any = None


# 1.2. Instancia global para reutilizar el modelo entre ejecuciones.
runtime_state = SimilarityRuntimeState()
