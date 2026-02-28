
from fastapi import APIRouter, HTTPException, status

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
from app.service.prompt_service import prompt_service

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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
