# --- DEPENDENCIAS ---
from fastapi import APIRouter

router = APIRouter(
    prefix="/gradio",
    tags=["Gradio"],
)


@router.get("/")
async def gradio():
    return {"gradio": "Gradio app launched successfully!"}
