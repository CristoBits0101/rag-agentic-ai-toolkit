# --- DEPENDENCIAS ---
# 1. Dataclass: Para definir el estado compartido del spike.
# 2. Any: Para tipar recursos externos sin acoplar el modulo.
from dataclasses import dataclass
from typing import Any

# --- ESTADO ---
# 1.1. Clase que centraliza cliente y coleccion activos.
@dataclass
class ChromaDbRuntimeState:
    client: Any = None
    collection: Any = None
    collection_name: str = ""


# 1.2. Instancia global para reutilizar recursos entre funciones.
runtime_state = ChromaDbRuntimeState()
