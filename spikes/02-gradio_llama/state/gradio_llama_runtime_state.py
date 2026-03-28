# --- DEPENDENCIAS ---
# 1. Dataclass: Para agrupar el estado de la practica.
# 2.       Any: Para guardar objetos cargados en tiempo de ejecucion.
from dataclasses import dataclass
from typing import Any


# --- ESTADO ---
# 1.1. Modelo de datos para el estado de la practica.
@dataclass
class GradioLlamaState:
    # Guarda el modelo Llama ya cargado.
    llama_model: Any = None


# 1.2. Instancia compartida del estado.
runtime_state = GradioLlamaState()
