# --- DEPENDENCIAS ---
# 1. Dataclass: Para definir el estado compartido del spike.
# 2. Any: Para tipar recursos externos sin acoplar el modulo.
from dataclasses import dataclass
from typing import Any

# --- ESTADO ---
# 1.1. Clase que centraliza cliente y colecciones activas.
@dataclass
class EmployeeSimilarityState:
    client: Any = None
    employee_collection: Any = None
    book_collection: Any = None


# 1.2. Instancia global para reutilizar recursos entre funciones.
runtime_state = EmployeeSimilarityState()
