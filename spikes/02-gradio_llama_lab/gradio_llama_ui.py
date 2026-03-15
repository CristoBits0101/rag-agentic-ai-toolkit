# --- DEPENDENCIAS ---
# 1. Gradio: Para construir la interfaz visual.
# 2.  Pasos: Para conectar la interfaz con la logica.
import gradio as gr

from gradio_llama_steps import add_numbers
from gradio_llama_steps import build_sentence
from gradio_llama_steps import run_llama_step


# Construye la interfaz completa de la practica.
def build_demo():
    # Crea el contenedor principal de la aplicacion.
    with gr.Blocks(title="Practica 02 Gradio con Llama") as demo:
        # Muestra una guia rapida en la parte superior.
        gr.Markdown(
            """
# Practica 02: Gradio con Llama.
Paso 1: Prueba una interaccion numerica simple.
Paso 2: Prueba componentes de formulario.
Paso 3: Ejecuta Llama local para una tarea concreta.
Requisito: Ejecuta `ollama serve` y descarga `llama3.2:3b`.
"""
        )

        # Crea la seccion del primer ejercicio.
        with gr.Accordion("Paso 1: Sumadora.", open=True):
            # Agrupa las entradas numericas en una fila.
            with gr.Row():
                first_number = gr.Number(label="Numero 1", value=1)
                second_number = gr.Number(label="Numero 2", value=2)

            sum_output = gr.Number(label="Resultado")
            sum_button = gr.Button("Sumar")
            sum_button.click(
                fn=add_numbers,
                inputs=[first_number, second_number],
                outputs=sum_output,
            )

        # Crea la seccion del formulario guiado.
        with gr.Accordion("Paso 2: Constructor de frase.", open=True):
            quantity = gr.Slider(1, 10, value=3, step=1, label="Cantidad")
            role = gr.Dropdown(
                choices=["Data Scientist", "Software Developer", "Software Engineer"],
                value="Software Developer",
                label="Rol",
            )
            countries = gr.CheckboxGroup(
                choices=["Canada", "Japan", "France"],
                value=["Canada"],
                label="Paises",
            )
            place = gr.Radio(
                choices=["la oficina", "el restaurante", "la sala de reunion"],
                value="la oficina",
                label="Lugar",
            )
            activities = gr.Dropdown(
                choices=["brainstormed", "coded", "fixed bugs", "partied"],
                value=["brainstormed"],
                multiselect=True,
                label="Actividades",
            )
            morning = gr.Checkbox(label="Manana")
            sentence_output = gr.Textbox(label="Frase")
            sentence_button = gr.Button("Construir frase")
            sentence_button.click(
                fn=build_sentence,
                inputs=[quantity, role, countries, place, activities, morning],
                outputs=sentence_output,
            )

        # Crea la seccion para usar el modelo local.
        with gr.Accordion("Paso 3: Llama local.", open=True):
            goal = gr.Dropdown(
                choices=["Explicar", "Resumir", "Traducir"],
                value="Explicar",
                label="Objetivo",
            )
            user_text = gr.Textbox(
                label="Texto o pregunta",
                lines=6,
                placeholder="Escribe aqui el contenido para Llama.",
            )
            llama_output = gr.Textbox(label="Respuesta", lines=10)
            llama_button = gr.Button("Ejecutar Llama")
            llama_button.click(
                fn=run_llama_step,
                inputs=[goal, user_text],
                outputs=llama_output,
            )

    # Devuelve la app lista para launch.
    return demo
