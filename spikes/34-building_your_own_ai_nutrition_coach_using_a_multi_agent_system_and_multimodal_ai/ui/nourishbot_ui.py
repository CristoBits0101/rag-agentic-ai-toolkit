# --- DEPENDENCIAS ---
import gradio as gr

from config.nourishbot_config import DEFAULT_DIETARY_PREFERENCE
from config.nourishbot_config import DEFAULT_WORKFLOW
from config.nourishbot_config import GRADIO_HOST
from config.nourishbot_config import GRADIO_PORT
from config.nourishbot_config import SUPPORTED_DIETARY_PREFERENCES
from orchestration.nourishbot_asset_orchestration import ensure_example_assets
from orchestration.nourishbot_workflow import analyze_pil_image

THEME = gr.themes.Soft(primary_hue="green", secondary_hue="amber")
CSS = """
.hero {
    text-align: center;
    font-size: 1.8rem;
    letter-spacing: 0.04em;
    color: #355c4a;
}
.subhero {
    text-align: center;
    color: #4d5f52;
}
"""


def build_nourishbot_interface():
    assets = ensure_example_assets()
    examples = [
        [str(assets["salmon_power_bowl"]), "balanced", "analysis"],
        [str(assets["veggie_buddha_bowl"]), "vegan", "recipe"],
        [str(assets["chicken_stir_fry"]), "high-protein", "analysis"],
    ]

    with gr.Blocks() as demo:
        gr.Markdown("# NourishBot Multi Agent Nutrition Coach", elem_classes="hero")
        gr.Markdown(
            "Upload a meal image and choose whether you want nutritional analysis or a dietary aware recipe remix.",
            elem_classes="subhero",
        )
        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(type="pil", label="Meal Image")
                dietary_input = gr.Dropdown(
                    choices=list(SUPPORTED_DIETARY_PREFERENCES),
                    value=DEFAULT_DIETARY_PREFERENCE,
                    label="Dietary Preference",
                )
                workflow_input = gr.Radio(["analysis", "recipe"], value=DEFAULT_WORKFLOW, label="Workflow")
                submit_button = gr.Button("Analyze")
            with gr.Column(scale=2):
                result_output = gr.Markdown("Results will appear here.")
                gr.Examples(examples=examples, inputs=[image_input, dietary_input, workflow_input], label="Sample Meals")

        submit_button.click(fn=analyze_pil_image, inputs=[image_input, dietary_input, workflow_input], outputs=result_output)

    return demo


def launch_nourishbot_interface() -> None:
    demo = build_nourishbot_interface()
    demo.launch(server_name=GRADIO_HOST, server_port=GRADIO_PORT, theme=THEME, css=CSS)