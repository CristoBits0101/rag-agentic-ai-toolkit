# --- DEPENDENCIAS ---
# 1.    Gradio: Para construir la interfaz visual de carga y consulta.
# 2. RAG QA PDF: Para responder preguntas usando el PDF cargado.
import gradio as gr

from orchestration.rag_orchestration_qa import rag_qa

# --- INTERFAZ ---
# 1.1. Funcion para construir la interfaz web de la practica.
def build_interface():
    # Crea la interfaz web de la practica.
    rag_application = gr.Interface(
        # Usa la funcion principal para procesar la consulta.
        fn=rag_qa,
        # Desactiva el marcado manual de respuestas.
        flagging_mode="never",
        # Define los campos de entrada de la interfaz.
        inputs=[
            gr.File(
                # Muestra el nombre del campo para el archivo.
                label="Upload PDF File",
                # Permite subir un solo archivo.
                file_count="single",
                # Limita la subida a archivos PDF.
                file_types=[".pdf"],
                # Entrega la ruta del archivo al codigo.
                type="filepath",
            ),
            gr.Textbox(
                # Muestra el nombre del campo para la pregunta.
                label="Input Query",
                # Da dos lineas de altura al cuadro.
                lines=2,
                # Muestra un texto de ayuda dentro del cuadro.
                placeholder="Type your question here...",
            ),
        ],
        # Define el cuadro donde se mostrara la respuesta.
        outputs=gr.Textbox(label="Output"),
        # Muestra el titulo principal de la app.
        title="RAG Chatbot",
        # Explica al usuario para que sirve la interfaz.
        description=(
            "Upload a PDF document and ask any question. "
            "The chatbot will try to answer using the provided document."
        ),
    )

    # Devuelve la interfaz lista para ejecutar.
    return rag_application
