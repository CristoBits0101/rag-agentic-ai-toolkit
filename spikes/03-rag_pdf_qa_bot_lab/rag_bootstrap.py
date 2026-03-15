# --- DEPENDENCIAS ---
# 1. Warnings: Para ocultar avisos durante la practica.
import warnings

# --- WARNINGS ---
# 1.1. Funcion para ocultar warnings durante la ejecucion de la practica.
def warn(*args, **kwargs):
    # Ignora avisos no criticos para mantener la salida mas limpia.
    pass


# 1.2. Funcion para aplicar la configuracion de warnings.
def configure_warnings():
    # Reemplaza la funcion original de warnings.
    warnings.warn = warn
    # Oculta los warnings durante la practica.
    warnings.filterwarnings("ignore")
