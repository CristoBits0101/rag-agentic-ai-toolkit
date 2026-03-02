# --- DEPENDENCIAS ---

# APIRouter para definir las rutas específicas de los endpoint.
# HTTPException y status para manejar errores de manera adecuada en las respuestas.
from fastapi import APIRouter, HTTPException, status

# --- ESQUEMAS DE SOLICITUD Y RESPUESTA ---

# Importamos los esquemas de solicitud y respuesta para cada ejercicio y para la completación de prompts.
from app.modules.features.chatbot.schemas import (
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

# --- SERVICIO DE PROMPTS ---

# Importamos el servicio que contiene la lógica de negocio para manejar las solicitudes relacionadas con prompts y ejercicios. 
from app.modules.features.chatbot.service import prompt_service

# --- PREFIJO DE ENDPOINTS DE PROMPTS ---

# Definimos el prefijo para todas las rutas de este endpoint y la etiqueta para la documentación automática.
router = APIRouter(prefix="/prompt", tags=["Prompt"])

# --- ENDPOINTS DE PROMPTS ---

# Ejercicio 1: 
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

# Ejercicio 2:
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

# Ejercicio 3: 
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

# Ejercicio 4: 
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

# Ejercicio 5: 
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
