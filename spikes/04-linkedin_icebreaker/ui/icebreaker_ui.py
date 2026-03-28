# --- DEPENDENCIAS ---
# 1. Gradio: Para construir la interfaz visual del spike.
# 2. Configuracion: Para leer perfiles y modelos por defecto.
# 3. Orquestacion: Para procesar perfiles y atender el chat.
# 4. Pipeline: Para poblar el selector de perfiles mock.
import gradio as gr

from config.icebreaker_config import DEFAULT_LLM_MODEL
from config.icebreaker_config import DEFAULT_PROFILE_KEY
from config.icebreaker_config import LLM_MODEL_OPTIONS
from orchestration.icebreaker_orchestration_profile import chat_with_profile
from orchestration.icebreaker_orchestration_profile import process_profile
from pipeline.icebreaker_profile_pipeline import list_profile_choices

# --- INTERFAZ ---
# 1.1. Funcion para construir la interfaz Gradio de la practica.
def build_interface():
    # Calcula las opciones visibles de perfiles demo.
    profile_choices = list_profile_choices()

    # Construye la interfaz completa del spike.
    with gr.Blocks(title="Practica 04 LinkedIn Icebreaker con Ollama") as demo:
        gr.Markdown(
            """
# Practica 04: LinkedIn Icebreaker con Ollama.
Paso 1: Selecciona un perfil mock tipo LinkedIn.
Paso 2: Genera tres hechos interesantes con RAG.
Paso 3: Haz preguntas sobre experiencia educacion habilidades o logros.
Requisito: Ejecuta `ollama serve` y descarga `llama3.2:3b` y `nomic-embed-text`.
"""
        )
        active_profile = gr.State(value="")
        active_model = gr.State(value=DEFAULT_LLM_MODEL)

        with gr.Tab("Procesar perfil"):
            with gr.Row():
                with gr.Column():
                    profile_dropdown = gr.Dropdown(
                        choices=profile_choices,
                        value=DEFAULT_PROFILE_KEY,
                        label="Perfil demo",
                    )
                    model_dropdown = gr.Dropdown(
                        choices=LLM_MODEL_OPTIONS,
                        value=DEFAULT_LLM_MODEL,
                        label="Modelo Ollama",
                    )
                    process_button = gr.Button("Procesar perfil")

                with gr.Column():
                    facts_output = gr.Textbox(
                        label="Resumen inicial",
                        lines=14,
                    )

        with gr.Tab("Chat"):
            gr.Markdown("Haz preguntas sobre el perfil ya procesado.")
            chatbot = gr.Chatbot(height=420)
            chat_input = gr.Textbox(
                label="Pregunta",
                lines=2,
                placeholder="Pregunta por experiencia educacion o habilidades.",
            )
            chat_button = gr.Button("Preguntar")

        process_button.click(
            fn=process_profile,
            inputs=[profile_dropdown, model_dropdown],
            outputs=[facts_output, active_profile, active_model, chatbot],
        )
        chat_button.click(
            fn=chat_with_profile,
            inputs=[active_profile, active_model, chat_input, chatbot],
            outputs=[chatbot, chat_input],
        )
        chat_input.submit(
            fn=chat_with_profile,
            inputs=[active_profile, active_model, chat_input, chatbot],
            outputs=[chatbot, chat_input],
        )

    # Devuelve la interfaz lista para launch.
    return demo
