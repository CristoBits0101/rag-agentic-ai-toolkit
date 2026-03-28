# --- DEPENDENCIAS ---
import gradio as gr

from config.style_finder_fashion_config import STYLE_FINDER_DEFAULT_MODEL
from config.style_finder_fashion_config import STYLE_FINDER_GRADIO_HOST
from config.style_finder_fashion_config import STYLE_FINDER_GRADIO_PORT
from config.style_finder_fashion_config import STYLE_FINDER_SUPPORTED_MODELS


def build_style_finder_interface(app):
    example_paths = [str(path) for path in app.example_image_paths.values()]

    with gr.Blocks(title="Style Finder Fashion RAG") as demo:
        gr.Markdown(
            """
            # Style Finder Fashion RAG

            Upload a fashion image to run a multimodal retrieval pipeline.
            The app compares your image against a local fashion dataset and then asks a real vision model for a catalog style analysis.
            """
        )

        with gr.Row():
            image_input = gr.Image(type="pil", label="Upload Fashion Image")
            with gr.Column():
                model_input = gr.Dropdown(
                    choices=list(STYLE_FINDER_SUPPORTED_MODELS),
                    value=STYLE_FINDER_DEFAULT_MODEL,
                    label="Vision Model",
                )
                submit_button = gr.Button("Analyze Style", variant="primary")
                status_output = gr.Markdown("Ready to analyze.")

        gr.Examples(
            examples=example_paths,
            inputs=image_input,
            label="Example Looks",
        )

        output = gr.Markdown(label="Style Analysis Results", height=600)

        submit_button.click(
            fn=lambda: "Analyzing image and retrieving similar fashion items.",
            inputs=None,
            outputs=status_output,
        ).then(
            fn=app.process_image,
            inputs=[image_input, model_input],
            outputs=output,
        ).then(
            fn=lambda: "Analysis complete.",
            inputs=None,
            outputs=status_output,
        )

        gr.Markdown(
            """
            ### Pipeline

            - Image encoding and vectorization for similarity search.
            - Retrieval of related outfit items from a structured dataset.
            - Context augmented response generation with a real vision model.
            """
        )

    return demo


def launch_style_finder_interface(app):
    build_style_finder_interface(app).launch(
        server_name=STYLE_FINDER_GRADIO_HOST,
        server_port=STYLE_FINDER_GRADIO_PORT,
    )
