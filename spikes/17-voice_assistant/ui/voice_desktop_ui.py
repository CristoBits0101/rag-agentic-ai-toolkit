# --- DEPENDENCIAS ---
import threading
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk

from config.voice_desktop_config import VOICE_RESPONSE_ENABLED_BY_DEFAULT
from config.voice_desktop_config import UI_WINDOW_SIZE
from config.voice_desktop_config import UI_WINDOW_TITLE
from models.voice_microphone_gateway import ContinuousAudioChannel
from models.voice_local_tts_gateway import LocalVoiceSpeaker
from models.voice_microphone_gateway import ManualAudioRecorder
from models.voice_transcription_gateway import transcribe_audio_file
from orchestration.voice_desktop_session_orchestration import process_voice_transcript
from orchestration.voice_desktop_session_orchestration import should_exit_session


def build_status_message(message: str) -> str:
    compact_message = " ".join((message or "").split())
    if not compact_message:
        return "Sin informacion."

    sentence_indexes = [
        compact_message.find(separator)
        for separator in (". ", "! ", "? ")
        if compact_message.find(separator) != -1
    ]
    if not sentence_indexes:
        return compact_message

    first_sentence_end = min(sentence_indexes)
    return compact_message[: first_sentence_end + 1]


def build_channel_button_label(channel_open: bool) -> str:
    return "Apagar" if channel_open else "Hablar"


def should_ignore_global_space_shortcut(widget) -> bool:
    if widget is None:
        return False

    try:
        widget_class = widget.winfo_class()
    except Exception:
        return False

    return widget_class in {"Entry", "TEntry", "Text"}


@dataclass(slots=True)
class VoiceDesktopTurn:
    transcript: str
    assistant_message: str
    exit_requested: bool = False


class VoiceDesktopController:
    def __init__(
        self,
        recorder_factory=ManualAudioRecorder,
        channel_factory=ContinuousAudioChannel,
        transcriber=transcribe_audio_file,
        transcript_processor=process_voice_transcript,
        exit_checker=should_exit_session,
    ) -> None:
        self.recorder_factory = recorder_factory
        self.channel_factory = channel_factory
        self.transcriber = transcriber
        self.transcript_processor = transcript_processor
        self.exit_checker = exit_checker
        self.pending_plan = None
        self.recorder = None
        self.channel = None
        self.is_recording = False

    def start_recording(self) -> str:
        if self.is_recording:
            return "La grabacion ya esta en curso."

        self.recorder = self.recorder_factory()
        self.recorder.start()
        self.is_recording = True
        return "Escuchando."

    def stop_recording_and_process(self) -> VoiceDesktopTurn:
        if not self.is_recording or self.recorder is None:
            raise RuntimeError("Recording has not started.")

        recorder = self.recorder
        self.recorder = None
        self.is_recording = False
        audio_path = recorder.stop()
        transcript = self.transcriber(audio_path)
        return self.submit_transcript(transcript)

    def cancel_recording(self) -> None:
        if not self.is_recording or self.recorder is None:
            return

        recorder = self.recorder
        self.recorder = None
        self.is_recording = False
        recorder.stop()

    def open_channel(self) -> str:
        if self.channel is not None:
            return "El canal ya esta abierto."

        self.channel = self.channel_factory()
        self.channel.start()
        return "Canal abierto. Escuchando."

    def close_channel(self) -> str:
        if self.channel is None:
            return "El canal ya esta cerrado."

        channel = self.channel
        self.channel = None
        channel.stop()
        return "Canal cerrado."

    def listen_once_and_process(self) -> VoiceDesktopTurn | None:
        if self.channel is None:
            raise RuntimeError("Voice channel has not started.")

        audio_path = self.channel.capture_next_utterance()
        if audio_path is None:
            return None

        transcript = self.transcriber(audio_path)
        return self.submit_transcript(transcript)

    def submit_transcript(self, transcript: str) -> VoiceDesktopTurn:
        if self.exit_checker(transcript):
            return VoiceDesktopTurn(
                transcript=transcript,
                assistant_message="Sesion cerrada.",
                exit_requested=True,
            )

        result, self.pending_plan = self.transcript_processor(
            transcript,
            pending_plan=self.pending_plan,
        )
        return VoiceDesktopTurn(
            transcript=transcript,
            assistant_message=result.message,
            exit_requested=False,
        )


class VoiceDesktopAssistantApp:
    def __init__(
        self,
        controller: VoiceDesktopController | None = None,
        speaker: LocalVoiceSpeaker | None = None,
    ) -> None:
        self.controller = controller or VoiceDesktopController()
        self.speaker = speaker or LocalVoiceSpeaker()
        self.root = tk.Tk()
        self.root.title(UI_WINDOW_TITLE)
        self.root.geometry(UI_WINDOW_SIZE)
        self.root.minsize(840, 560)
        self.status_var = tk.StringVar(value="Canal cerrado. Pulsa el boton o la barra espaciadora para abrirlo.")
        self.recording_var = tk.StringVar(value=build_channel_button_label(channel_open=False))
        self.manual_message_var = tk.StringVar(value="")
        self.voice_enabled_var = tk.BooleanVar(
            value=VOICE_RESPONSE_ENABLED_BY_DEFAULT and self.speaker.is_available()
        )
        self.processing = False
        self.channel_visual_open = False
        self.space_pressed = False
        self.channel_thread = None
        self._build_layout()
        self._bind_shortcuts()
        self._sync_channel_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._close_app)

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)

        title = ttk.Label(
            container,
            text="Voice Desktop Assistant",
            font=("Segoe UI", 20, "bold"),
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            container,
            text="Comandos seguros de escritorio con micro local Whisper Ollama y confirmacion antes de borrar.",
            wraplength=840,
        )
        subtitle.pack(anchor="w", pady=(8, 16))

        controls = ttk.Frame(container)
        controls.pack(fill="x")
        button_width = 12

        channel_frame = ttk.Frame(controls)
        channel_frame.pack(side="left")

        self.channel_indicator = tk.Canvas(
            channel_frame,
            width=28,
            height=28,
            highlightthickness=0,
            borderwidth=0,
            background=self.root.cget("bg"),
        )
        self.channel_indicator.pack(side="left")
        self.channel_indicator_item = self.channel_indicator.create_oval(4, 4, 24, 24, fill="#c93b3b", outline="#8a1f1f", width=2)

        self.record_button = ttk.Button(
            controls,
            textvariable=self.recording_var,
            width=button_width,
            command=self._toggle_channel,
            takefocus=False,
        )
        self.record_button.pack(side="left", padx=(12, 0))

        self.confirm_button = ttk.Button(
            controls,
            text="Confirmar",
            width=button_width,
            command=lambda: self._process_manual_transcript("confirmar"),
            takefocus=False,
        )
        self.confirm_button.pack(side="left", padx=(12, 0))

        self.cancel_button = ttk.Button(
            controls,
            text="Cancelar",
            width=button_width,
            command=lambda: self._process_manual_transcript("cancelar"),
            takefocus=False,
        )
        self.cancel_button.pack(side="left", padx=(12, 0))

        self.voice_toggle = ttk.Checkbutton(
            controls,
            text="Responder con voz",
            variable=self.voice_enabled_var,
            takefocus=False,
        )
        self.voice_toggle.pack(side="left", padx=(12, 0))

        self.close_button = ttk.Button(
            controls,
            text="Salir",
            width=button_width,
            command=self._close_app,
            takefocus=False,
        )
        self.close_button.pack(side="right")

        status_frame = ttk.Frame(container)
        status_frame.pack(fill="x", pady=(16, 12))

        status_label = ttk.Label(status_frame, text="Estado", font=("Segoe UI", 10, "bold"))
        status_label.pack(anchor="w")

        status_value = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            wraplength=840,
        )
        status_value.pack(anchor="w", pady=(6, 0))

        message_frame = ttk.Frame(container)
        message_frame.pack(fill="x", pady=(0, 12))

        message_label = ttk.Label(message_frame, text="Mensaje", font=("Segoe UI", 10, "bold"))
        message_label.pack(anchor="w")

        message_controls = ttk.Frame(message_frame)
        message_controls.pack(fill="x", pady=(6, 0))

        self.manual_message_entry = ttk.Entry(
            message_controls,
            textvariable=self.manual_message_var,
        )
        self.manual_message_entry.pack(side="left", fill="x", expand=True)
        self.manual_message_entry.bind("<Return>", self._submit_text_message)

        self.send_button = ttk.Button(
            message_controls,
            text="Enviar",
            width=button_width,
            command=self._submit_text_message,
            takefocus=False,
        )
        self.send_button.pack(side="left", padx=(12, 0))

        history_label = ttk.Label(container, text="Historial", font=("Segoe UI", 10, "bold"))
        history_label.pack(anchor="w")

        self.history_outer = tk.Frame(
            container,
            bg="#b6b6b6",
            highlightbackground="#b6b6b6",
            highlightthickness=1,
        )
        self.history_outer.pack(fill="both", expand=True, pady=(8, 0))

        self.history_scrollbar = ttk.Scrollbar(self.history_outer, orient="vertical")
        self.history_scrollbar.pack(side="right", fill="y")

        self.history = tk.Text(
            self.history_outer,
            wrap="word",
            background="white",
            font=("Consolas", 11),
            borderwidth=0,
            highlightthickness=0,
            padx=2,
            pady=2,
            insertwidth=0,
            cursor="xterm",
        )
        self.history.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        self.history_scrollbar.configure(command=self.history.yview)
        self.history.configure(yscrollcommand=self.history_scrollbar.set)
        self.history.tag_configure("assistant_message", spacing3=1)
        self.history.tag_configure("user_message", spacing3=1)
        self.history.bind("<Key>", lambda _event: "break")

        self._append_history(
            "Asistente",
            "Usa el boton o la barra espaciadora para abrir o cerrar el canal de voz.",
        )
        self._append_history(
            "Asistente",
            "Las acciones de papelera siempre requieren confirmacion.",
        )
        if not self.speaker.is_available():
            self.voice_toggle.configure(state="disabled")
            self.status_var.set("La respuesta por voz local no esta disponible. La app seguira en modo texto.")

    def _bind_shortcuts(self) -> None:
        self.root.bind_all("<KeyPress-space>", self._handle_space_press)
        self.root.bind_all("<KeyRelease-space>", self._handle_space_release)
        self.root.after(100, self.root.focus_force)

    def _set_processing(self, enabled: bool) -> None:
        self.processing = enabled
        next_state = "disabled" if enabled else "normal"
        self.record_button.configure(state=next_state)
        self.confirm_button.configure(state=next_state)
        self.cancel_button.configure(state=next_state)
        self.send_button.configure(state=next_state)
        self.manual_message_entry.configure(state=next_state)

    def _sync_channel_ui(self) -> None:
        self.recording_var.set(build_channel_button_label(self.channel_visual_open))
        if self.channel_visual_open:
            self.channel_indicator.itemconfig(
                self.channel_indicator_item,
                fill="#19c37d",
                outline="#0e8f58",
            )
            return

        self.channel_indicator.itemconfig(
            self.channel_indicator_item,
            fill="#c93b3b",
            outline="#8a1f1f",
        )

    def _scroll_history_to_end(self) -> None:
        self.history.see("end")

    def _append_history(self, speaker: str, message: str) -> None:
        tag_name = "assistant_message" if speaker == "Asistente" else "user_message"
        self.history.configure(state="normal")
        self.history.insert("end", f"{speaker}: {message}\n", tag_name)
        self.history.configure(state="disabled")
        self.root.after_idle(self._scroll_history_to_end)

    def _open_channel(self) -> None:
        if self.processing:
            return

        self.speaker.stop()
        try:
            message = self.controller.open_channel()
        except Exception as exc:
            self.status_var.set(build_status_message(str(exc)))
            self._append_history("Asistente", str(exc))
            return

        self.channel_visual_open = True
        self._sync_channel_ui()
        self.status_var.set(message)
        self.channel_thread = threading.Thread(target=self._channel_worker, daemon=True)
        self.channel_thread.start()

    def _close_channel(self) -> None:
        if self.processing:
            return

        try:
            message = self.controller.close_channel()
        except Exception as exc:
            self.status_var.set(build_status_message(str(exc)))
            self._append_history("Asistente", str(exc))
            return

        self.channel_visual_open = False
        self._sync_channel_ui()
        self.status_var.set(message)

    def _toggle_channel(self) -> None:
        if self.processing:
            return

        if self.controller.channel is not None:
            self._close_channel()
            return

        self._open_channel()

    def _handle_space_press(self, _event=None):
        if should_ignore_global_space_shortcut(self.root.focus_get()):
            return None

        if self.space_pressed:
            return "break"

        self.space_pressed = True
        self._toggle_channel()
        return "break"

    def _handle_space_release(self, _event=None):
        if should_ignore_global_space_shortcut(self.root.focus_get()):
            return None

        self.space_pressed = False
        return "break"

    def _recording_worker(self) -> None:
        try:
            turn = self.controller.stop_recording_and_process()
        except Exception as exc:
            message = str(exc)
            self.root.after(0, lambda message=message: self._finish_with_error(message))
            return

        self.root.after(0, lambda: self._finish_turn(turn))

    def _channel_worker(self) -> None:
        while self.controller.channel is not None:
            try:
                turn = self.controller.listen_once_and_process()
            except Exception as exc:
                message = str(exc)
                self.root.after(0, lambda message=message: self._finish_with_error(message))
                return

            if turn is None:
                if self.controller.channel is None:
                    return
                continue

            self.root.after(0, lambda turn=turn: self._finish_turn(turn, keep_channel_open=True))
            if turn.exit_requested:
                return

    def _process_manual_transcript(self, transcript: str, status_message: str = "Procesando la accion manual.") -> None:
        if self.processing or self.controller.is_recording:
            return

        self.speaker.stop()
        self._set_processing(True)
        self.status_var.set(status_message)

        def worker() -> None:
            try:
                turn = self.controller.submit_transcript(transcript)
            except Exception as exc:
                message = str(exc)
                self.root.after(0, lambda message=message: self._finish_with_error(message))
                return

            self.root.after(0, lambda: self._finish_turn(turn))

        threading.Thread(target=worker, daemon=True).start()

    def _submit_text_message(self, _event=None):
        if self.processing or self.controller.is_recording:
            return "break"

        transcript = self.manual_message_var.get().strip()
        if not transcript:
            return "break"

        self.manual_message_var.set("")
        self._process_manual_transcript(
            transcript,
            status_message="Procesando el mensaje escrito.",
        )
        return "break"

    def _finish_with_error(self, message: str) -> None:
        self._set_processing(False)
        if self.controller.channel is not None:
            try:
                self.controller.close_channel()
            except Exception:
                pass
        self.channel_visual_open = False
        self._sync_channel_ui()
        self.status_var.set(build_status_message(message))
        self._append_history("Asistente", message)

    def _finish_turn(self, turn: VoiceDesktopTurn, keep_channel_open: bool = False) -> None:
        self._set_processing(False)
        self.channel_visual_open = keep_channel_open and self.controller.channel is not None
        self._sync_channel_ui()
        self._append_history("Tu", turn.transcript)
        self._append_history("Asistente", turn.assistant_message)
        if keep_channel_open and self.controller.channel is not None:
            self.status_var.set("Canal abierto. Escuchando.")
        else:
            self.status_var.set(build_status_message(turn.assistant_message))
        if self.voice_enabled_var.get() and not turn.exit_requested:
            try:
                self.speaker.speak_async(turn.assistant_message)
            except Exception:
                pass
        if turn.exit_requested:
            if self.controller.channel is not None:
                try:
                    self.controller.close_channel()
                except Exception:
                    pass
            self.root.after(300, self._close_app)

    def _close_app(self) -> None:
        self.speaker.stop()
        try:
            self.controller.cancel_recording()
        except Exception:
            pass
        try:
            self.controller.close_channel()
        except Exception:
            pass
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def launch_interface() -> None:
    app = VoiceDesktopAssistantApp()
    app.run()
