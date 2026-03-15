# --- DEPENDENCIAS ---
# 1.  Prompting Basico: Para ejecutar ejercicios de prompting directo.
# 2.              LCEL: Para ejecutar ejercicios con cadenas LCEL.
# 3.       Razonamiento: Para ejecutar el ejercicio de analisis estructurado.
from orchestration.prompting_orchestration_basic import run_baseline
from orchestration.prompting_orchestration_basic import run_exercise_3_step_by_step
from orchestration.prompting_orchestration_basic import run_few_shot
from orchestration.prompting_orchestration_basic import run_greeting_example
from orchestration.prompting_orchestration_basic import run_one_shot_prompts
from orchestration.prompting_orchestration_basic import run_task_prompts
from orchestration.prompting_orchestration_lcel import run_exercise_4_lcel
from orchestration.prompting_orchestration_reasoning import run_exercise_5_reasoning_and_reviews


# Ejecuta todos los ejercicios de la practica.
def run_all_exercises():
    # Ejecuta el ejemplo inicial de saludo.
    run_greeting_example()
    # Ejecuta el ejercicio base de prompting.
    run_baseline()
    # Ejecuta el bloque de prompts por tarea.
    run_task_prompts()
    # Ejecuta el bloque de one shot prompting.
    run_one_shot_prompts(
        "Escribe un correo formal para solicitar una reunion con un cliente la proxima semana.\n\nCorreo:",
        "Explica el concepto de aprendizaje automatico en terminos sencillos para un principiante.\n\nExplicacion:",
        "Extrae las palabras clave principales del siguiente texto:\nArtificial intelligence and machine learning are rapidly transforming industries worldwide.\n\nPalabras clave:",
    )
    # Ejecuta el bloque de few shot prompting.
    run_few_shot()
    # Ejecuta el ejercicio paso a paso.
    run_exercise_3_step_by_step()
    # Ejecuta el ejercicio de cadenas LCEL.
    run_exercise_4_lcel()
    # Ejecuta el ejercicio de razonamiento y analisis.
    run_exercise_5_reasoning_and_reviews()


if __name__ == "__main__":
    # Lanza todos los ejercicios cuando este archivo se ejecuta directamente.
    run_all_exercises()
