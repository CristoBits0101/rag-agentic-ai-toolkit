# --- DEPENDENCIAS ---
import gradio as gr

from config.meeting_assistant_config import GRADIO_HOST
from config.meeting_assistant_config import GRADIO_PORT
from orchestration.meeting_assistant_orchestration import transcript_audio


def build_interface():
    return gr.Interface(
        fn=transcript_audio,
        inputs=gr.Audio(sources="upload", type="filepath", label="Upload your audio file"),
        outputs=[
            gr.Textbox(label="Meeting Minutes and Tasks"),
            gr.File(label="Download the Generated Meeting Minutes and Tasks"),
        ],
        title="AI Meeting Assistant",
        description=(
            "Upload an audio file of a meeting. "
            "This tool transcribes the audio, normalizes key finance terms and generates meeting minutes with tasks."
        ),
    )


def launch_interface():
    build_interface().launch(server_name=GRADIO_HOST, server_port=GRADIO_PORT)
