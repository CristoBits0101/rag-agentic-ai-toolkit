# --- DEPENDENCIAS ---
# 1. Dataclass: Para definir el estado compartido del spike.
# 2. Any: Para tipar objetos externos sin acoplar el estado.
from dataclasses import dataclass
from typing import Any

# --- ESTADO ---
# 1.1. Clase que centraliza el estado reutilizable de la practica.
@dataclass
class IcebreakerState:
    embedding_model_name: str = ""
    active_profile_key: str = ""
    embedding_model: Any = None
    vector_store: Any = None
    retriever: Any = None


# 1.2. Instancia global para reutilizar recursos entre peticiones.
runtime_state = IcebreakerState()
