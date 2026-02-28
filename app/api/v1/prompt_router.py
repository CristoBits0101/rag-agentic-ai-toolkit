# --- DEPENDENCIAS ---


#     APIRouter: Permite organizar las rutas de la API en módulos separados.
# HTTPException: Permite manejar errores y devolver respuestas HTTP con códigos de estado específicos.
#        status: Proporciona constantes para códigos de estado HTTP.
from fastapi import APIRouter, HTTPException, status

# Importamos los modelos de datos para las solicitudes y respuestas de cada ejercicio.
# Se utilizan para validar y estructurar los datos que se envían y reciben a través de la API.
from app.schemas.prompt_schemas import (
    Exercise2Request,
    Exercise2Response,
    Exercise3Request,
    Exercise3Response,
    Exercise4Request,
    Exercise4Response,
    Exercise5Request,
    Exercise5Response,
    PromptCompletionRequest,
    PromptCompletionResponse,
)

# Importamos el servicio que contiene la lógica de negocio para cada ejercicio.
# Este servicio se encargará de procesar las solicitudes y generar las respuestas correspondientes.
from app.services.prompt_service import prompt_service


# -- RUTAS DE LA API ---


# Creamos un router para organizar las rutas relacionadas con los prompts.
# El prefijo "/prompt" se añadirá a todas las rutas definidas en este router.
# Las etiquetas se utilizan para la documentación automática de la API.
router = APIRouter(
    prefix="/prompt",
    tags=["Prompt"],
)


@router.get("/")
async def prompt_health() -> dict[str, str]:
    return {"prompt": "Prompt service ready"}


# --- EJERCICIO 1: PROMPT ENGINEERING ---
@router.post("/exercise-1/completion", response_model=PromptCompletionResponse)
async def exercise_1_completion(
    payload: PromptCompletionRequest,
) -> PromptCompletionResponse:
    try:
        output = prompt_service.run_exercise_1(payload)
        return PromptCompletionResponse(output=output)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


# --- EJERCICIO 2: CREACION DE PROMPTS PARA TAREAS ESPECIFICAS ---
@router.post("/exercise-2/task-prompts", response_model=Exercise2Response)
async def exercise_2_task_prompts(payload: Exercise2Request) -> Exercise2Response:
    try:
        result = prompt_service.run_exercise_2(payload)
        return Exercise2Response(**result)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


# --- EJERCICIO 3: CREACION DE PROMPTS PASO A PASO ---
@router.post("/exercise-3/step-by-step", response_model=Exercise3Response)
async def exercise_3_step_by_step(payload: Exercise3Request) -> Exercise3Response:
    try:
        result = prompt_service.run_exercise_3(payload)
        return Exercise3Response(**result)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


# --- EJERCICIO 4: LOGICA LCEL ---
@router.post("/exercise-4/lcel", response_model=Exercise4Response)
async def exercise_4_lcel(payload: Exercise4Request) -> Exercise4Response:
    try:
        outputs = prompt_service.run_exercise_4(payload)
        return Exercise4Response(outputs=outputs)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


# --- EJERCICIO 5: RAZONAMIENTO GUIADO + ANALISIS ESTRUCTURADO ---
@router.post("/exercise-5/reasoning-reviews", response_model=Exercise5Response)
async def exercise_5_reasoning_reviews(payload: Exercise5Request) -> Exercise5Response:
    try:
        result = prompt_service.run_exercise_5(payload)
        return Exercise5Response(**result)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
