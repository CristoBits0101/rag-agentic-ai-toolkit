# --- DEPENDENCIAS ---
# 1. Dataclass: Para definir el estado compartido del spike.
# 2. Any: Para tipar recursos externos sin acoplar el modulo.
from dataclasses import dataclass
from typing import Any

# --- ESTADO ---
# 1.1. Clase que centraliza cliente coleccion y LLM opcional.
@dataclass
class FoodRecommendationState:
    client: Any = None
    collection: Any = None
    llm_model: Any = None
    llm_checked: bool = False


# 1.2. Instancia global para reutilizar recursos entre funciones.
runtime_state = FoodRecommendationState()
