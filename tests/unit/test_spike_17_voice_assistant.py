# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "17-voice_assistant"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from models.voice_agent_demo_planner import build_demo_action_plan
from models.voice_agent_demo_planner import build_rule_based_action_plan
from models.voice_agent_ollama_gateway import extract_plan_payload
from models.voice_agent_ollama_gateway import normalize_plan_payload
from models.voice_agent_ollama_gateway import select_best_available_ollama_model
from models.voice_desktop_entities import VoiceActionPlan
from models.voice_local_tts_gateway import LocalVoiceSpeaker
from models.voice_local_tts_gateway import build_windows_speech_command
from models.voice_local_tts_gateway import clean_text_for_speech
from models.voice_local_tts_gateway import resolve_windows_speech_shell
from models.voice_microphone_gateway import write_pcm_frames_to_wav
from models.voice_transcription_gateway import build_whisper_pipeline
from models.voice_transcription_gateway import load_wav_audio_for_whisper
from models.voice_transcription_gateway import transcribe_audio_file
from orchestration.voice_desktop_planning_orchestration import build_voice_action_plan
from orchestration import voice_desktop_session_orchestration as session_orchestration
from orchestration.voice_desktop_execution_orchestration import close_application
from orchestration.voice_desktop_execution_orchestration import click_target
from orchestration.voice_desktop_execution_orchestration import click_target_with_retries
from orchestration.voice_desktop_execution_orchestration import execute_voice_action
from orchestration.voice_desktop_execution_orchestration import is_process_running
from orchestration.voice_desktop_execution_orchestration import is_protected_path
from orchestration.voice_desktop_execution_orchestration import open_application
from orchestration.voice_desktop_execution_orchestration import trash_path
from ui.voice_desktop_ui import build_channel_button_label
from ui.voice_desktop_ui import build_status_message
from ui.voice_desktop_ui import should_ignore_global_space_shortcut
from ui.voice_desktop_ui import VoiceDesktopController


def test_select_best_available_ollama_model_prefers_desktop_control_model():
    selected_model = select_best_available_ollama_model(
        ["qwen2.5:7b", "qwen3-vl:30b", "llama3.2:3b"],
    )

    assert selected_model == "qwen3-vl:30b"


def test_extract_plan_payload_reads_json_inside_plain_text():
    payload = extract_plan_payload(
        'Respuesta:\n{"action":"open_url","parameters":{"url":"https://example.com"},"response":"abro","requires_confirmation":false,"confirmation_prompt":""}'
    )

    assert payload["action"] == "open_url"
    assert payload["parameters"]["url"] == "https://example.com"


def test_build_demo_action_plan_marks_trash_request_for_confirmation():
    plan = build_demo_action_plan('borra "C:\\Users\\demo\\Downloads\\draft.txt"')

    assert plan.action == "trash_path"
    assert plan.requires_confirmation is True
    assert "Downloads" in plan.parameters["path"]


def test_build_demo_action_plan_marks_close_request_for_confirmation():
    plan = build_demo_action_plan("cierra google chrome")

    assert plan.action == "close_application"
    assert plan.requires_confirmation is True
    assert plan.parameters["application"] == "chrome"


def test_build_demo_action_plan_detects_league_play_click():
    plan = build_demo_action_plan("dale a jugar en league of legends")

    assert plan.action == "click_target"
    assert plan.parameters["target"] == "league_play_button"


def test_build_rule_based_action_plan_detects_league_play_click_with_common_stt_variant():
    plan = build_rule_based_action_plan("dale a jugar a leaguea of legends")

    assert plan is not None
    assert plan.action == "click_target"
    assert plan.parameters["target"] == "league_play_button"


def test_build_rule_based_action_plan_detects_ranked_solo_duo_click():
    plan = build_rule_based_action_plan("pon clasificatoria solo duo")

    assert plan is not None
    assert plan.action == "click_target"
    assert plan.parameters["target"] == "league_ranked_solo_duo_option"


def test_build_rule_based_action_plan_detects_find_match_click():
    plan = build_rule_based_action_plan("encontrar partida")

    assert plan is not None
    assert plan.action == "click_target"
    assert plan.parameters["target"] == "league_find_match_button"


def test_build_rule_based_action_plan_detects_confirm_click():
    plan = build_rule_based_action_plan("confirmar")

    assert plan is not None
    assert plan.action == "click_target"
    assert plan.parameters["target"] == "league_confirm_button"


def test_build_rule_based_action_plan_detects_league_from_log_transcript():
    plan = build_rule_based_action_plan("puedes cerrar el log")

    assert plan is not None
    assert plan.action == "close_application"
    assert plan.parameters["application"] == "league_of_legends"


def test_build_rule_based_action_plan_detects_league_from_diage_of_legends_transcript():
    plan = build_rule_based_action_plan("puede cerrar diage of legends")

    assert plan is not None
    assert plan.action == "close_application"
    assert plan.parameters["application"] == "league_of_legends"


def test_normalize_plan_payload_maps_common_ollama_aliases():
    plan = normalize_plan_payload(
        {
            "action": "close_app",
            "parameters": {"application": "Google Chrome"},
            "response": "Google Chrome se cerrara.",
            "requires_confirmation": False,
            "confirmation_prompt": "",
        },
        planner_model="qwen2.5:7b",
    )

    assert plan.action == "close_application"
    assert plan.parameters["application"] == "chrome"
    assert plan.requires_confirmation is True


def test_normalize_plan_payload_infers_application_from_transcript():
    plan = normalize_plan_payload(
        {
            "action": "open_app",
            "parameters": {},
            "response": "Abro la calculadora.",
            "requires_confirmation": False,
            "confirmation_prompt": "",
        },
        planner_model="qwen2.5:7b",
        transcript="abre calculadora",
    )

    assert plan.action == "open_application"
    assert plan.parameters["application"] == "calculator"


def test_normalize_plan_payload_infers_click_target_from_transcript():
    plan = normalize_plan_payload(
        {
            "action": "click_target",
            "parameters": {},
            "response": "Pulso jugar.",
            "requires_confirmation": False,
            "confirmation_prompt": "",
        },
        planner_model="qwen2.5:7b",
        transcript="dale a jugar en lol",
    )

    assert plan.action == "click_target"
    assert plan.parameters["target"] == "league_play_button"


def test_build_voice_action_plan_falls_back_to_demo_on_invalid_ollama_plan(monkeypatch):
    def fake_ollama_planner(transcript: str):
        raise RuntimeError("invalid plan")

    from orchestration import voice_desktop_planning_orchestration as planning_orchestration

    monkeypatch.setattr(
        planning_orchestration,
        "plan_voice_command_with_ollama",
        fake_ollama_planner,
    )

    try:
        build_voice_action_plan("haz algo completamente distinto")
        assert False, "Expected build_voice_action_plan to raise when Ollama planning fails."
    except RuntimeError as exc:
        assert "invalid plan" in str(exc)


def test_build_voice_action_plan_prefers_direct_rule_for_league_play(monkeypatch):
    from orchestration import voice_desktop_planning_orchestration as planning_orchestration

    monkeypatch.setattr(
        planning_orchestration,
        "plan_voice_command_with_ollama",
        lambda transcript: (_ for _ in ()).throw(RuntimeError("Ollama should not be called.")),
    )

    plan = build_voice_action_plan("dale a jugar a leaguea of legends")

    assert plan.action == "click_target"
    assert plan.parameters["target"] == "league_play_button"


def test_execute_voice_action_types_text_with_stubbed_pyautogui():
    events: list[tuple[str, str]] = []

    class FakePyAutoGUI:
        def write(self, text: str, interval: float = 0.01) -> None:
            events.append(("write", text))

        def hotkey(self, *keys: str) -> None:
            events.append(("hotkey", "+".join(keys)))

    plan = VoiceActionPlan(action="type_text", parameters={"text": "hola mundo"})
    result = execute_voice_action(plan, pyautogui_module=FakePyAutoGUI())

    assert result.success is True
    assert events == [("write", "hola mundo")]


def test_build_rule_based_action_plan_detects_mouse_move():
    plan = build_rule_based_action_plan("mueve el raton a x 640 y 360")

    assert plan is not None
    assert plan.action == "move_mouse"
    assert plan.parameters == {"x": 640, "y": 360}


def test_build_rule_based_action_plan_detects_mouse_click():
    plan = build_rule_based_action_plan("haz click derecho en x 500 y 320")

    assert plan is not None
    assert plan.action == "click_mouse"
    assert plan.parameters == {"button": "right", "x": 500, "y": 320}


def test_execute_voice_action_moves_mouse_with_stubbed_pyautogui():
    events: list[tuple[str, object]] = []

    class FakePyAutoGUI:
        def moveTo(self, x: int, y: int, duration: float = 0.2) -> None:
            events.append(("moveTo", (x, y, duration)))

    plan = VoiceActionPlan(action="move_mouse", parameters={"x": 300, "y": 220})
    result = execute_voice_action(plan, pyautogui_module=FakePyAutoGUI())

    assert result.success is True
    assert events == [("moveTo", (300, 220, 0.2))]


def test_execute_voice_action_clicks_mouse_with_stubbed_pyautogui():
    events: list[tuple[str, object]] = []

    class FakePyAutoGUI:
        def click(self, x=None, y=None, button="left") -> None:
            events.append(("click", (x, y, button)))

    plan = VoiceActionPlan(
        action="click_mouse",
        parameters={"button": "right", "x": 480, "y": 260},
    )
    result = execute_voice_action(plan, pyautogui_module=FakePyAutoGUI())

    assert result.success is True
    assert events == [("click", (480, 260, "right"))]


def test_click_target_with_retries_retries_until_success():
    events: list[str] = []
    results = iter(
        [
            session_orchestration.VoiceExecutionResult(False, "missing", "click_target"),
            session_orchestration.VoiceExecutionResult(True, "clicked", "click_target"),
        ]
    )

    def fake_click_executor(target_name: str, pyautogui_module=None):
        events.append(target_name)
        return next(results)

    result = click_target_with_retries(
        target_name="riot_play_button",
        click_executor=fake_click_executor,
        sleep_fn=lambda seconds: None,
        retry_attempts=3,
        retry_delay_seconds=0,
    )

    assert result.success is True
    assert events == ["riot_play_button", "riot_play_button"]


def test_open_application_clicks_direct_play_when_visible():
    launched_commands: list[list[str]] = []
    clicked_targets: list[str] = []

    def fake_process_launcher(command):
        launched_commands.append(command)

    def fake_click_executor(target_name: str, pyautogui_module=None):
        clicked_targets.append(target_name)
        return session_orchestration.VoiceExecutionResult(
            success=True,
            message=f"clicked {target_name}",
            action="click_target",
        )

    result = open_application(
        "league_of_legends",
        process_launcher=fake_process_launcher,
        pyautogui_module=object(),
        click_executor=fake_click_executor,
        sleep_fn=lambda seconds: None,
        startup_delay_seconds=0,
        click_retry_attempts=1,
        click_retry_delay_seconds=0,
    )

    assert result.success is True
    assert launched_commands == [["cmd", "/c", "start", "", "riotclient://"]]
    assert clicked_targets == ["riot_play_button"]


def test_open_application_falls_back_to_league_startup_workflow_when_play_is_not_visible():
    launched_commands: list[list[str]] = []
    clicked_targets: list[str] = []

    def fake_process_launcher(command):
        launched_commands.append(command)

    def fake_click_executor(target_name: str, pyautogui_module=None):
        clicked_targets.append(target_name)
        if target_name == "riot_play_button" and len(clicked_targets) == 1:
            return session_orchestration.VoiceExecutionResult(
                success=False,
                message="No he encontrado el boton Jugar.",
                action="click_target",
            )
        return session_orchestration.VoiceExecutionResult(
            success=True,
            message=f"clicked {target_name}",
            action="click_target",
        )

    result = open_application(
        "league_of_legends",
        process_launcher=fake_process_launcher,
        pyautogui_module=object(),
        click_executor=fake_click_executor,
        sleep_fn=lambda seconds: None,
        startup_delay_seconds=0,
        click_retry_attempts=1,
        click_retry_delay_seconds=0,
    )

    assert result.success is True
    assert launched_commands == [["cmd", "/c", "start", "", "riotclient://"]]
    assert clicked_targets == ["riot_play_button", "riot_lol_icon", "riot_play_button"]


def test_open_application_reports_failed_league_startup_workflow():
    launched_commands: list[list[str]] = []
    clicked_targets: list[str] = []

    def fake_process_launcher(command):
        launched_commands.append(command)

    def fake_click_executor(target_name: str, pyautogui_module=None):
        clicked_targets.append(target_name)
        if target_name == "riot_play_button" and len(clicked_targets) == 1:
            return session_orchestration.VoiceExecutionResult(
                success=False,
                message="No he encontrado el boton Jugar.",
                action="click_target",
            )
        if target_name == "riot_lol_icon":
            return session_orchestration.VoiceExecutionResult(
                success=False,
                message="No he encontrado el icono.",
                action="click_target",
            )
        return session_orchestration.VoiceExecutionResult(
            success=True,
            message=f"clicked {target_name}",
            action="click_target",
        )

    result = open_application(
        "league_of_legends",
        process_launcher=fake_process_launcher,
        pyautogui_module=object(),
        click_executor=fake_click_executor,
        sleep_fn=lambda seconds: None,
        startup_delay_seconds=0,
        click_retry_attempts=1,
        click_retry_delay_seconds=0,
    )

    assert result.success is False
    assert launched_commands == [["cmd", "/c", "start", "", "riotclient://"]]
    assert clicked_targets == ["riot_play_button", "riot_lol_icon"]
    assert "riot_lol_icon" in result.message


def test_click_target_uses_visual_match_and_clicks(tmp_path):
    template_file = tmp_path / "league_play_button.png"
    template_file.write_bytes(b"fake-png")
    events: list[tuple[str, object]] = []

    class Match:
        x = 320
        y = 240

    class FakePyAutoGUI:
        def locateCenterOnScreen(self, path: str, confidence: float = 0.9):
            events.append(("locate", Path(path).name))
            return Match()

        def click(self, x: int, y: int) -> None:
            events.append(("click", (x, y)))

    result = click_target(
        "league_play_button",
        click_targets={
            "league_play_button": {
                "display_name": "Boton Jugar de League of Legends",
                "template_paths": ("league_play_button.png",),
            }
        },
        pyautogui_module=FakePyAutoGUI(),
        project_root=tmp_path,
    )

    assert result.success is True
    assert events == [("locate", "league_play_button.png"), ("click", (320, 240))]


def test_click_target_reports_missing_template_or_hidden_target(tmp_path):
    events: list[tuple[str, object]] = []

    class FakePyAutoGUI:
        def locateCenterOnScreen(self, path: str, confidence: float = 0.9):
            return None

        def click(self, x: int, y: int) -> None:
            events.append(("click", (x, y)))

    result = click_target(
        "league_play_button",
        click_targets={
            "league_play_button": {
                "display_name": "Boton Jugar de League of Legends",
                "template_paths": ("missing.png",),
                "vision_prompt": "Boton JUGAR de League of Legends.",
            }
        },
        pyautogui_module=FakePyAutoGUI(),
        project_root=tmp_path,
        encoded_screen_provider=lambda: "encoded-screen",
        vision_locator=lambda target_name, target_description, encoded_image: {
            "found": False,
            "x": 0,
            "y": 0,
            "confidence": 0.0,
            "reason": "El objetivo no esta visible.",
            "model_name": "qwen3-vl:30b",
        },
    )

    assert result.success is False
    assert "No he encontrado" in result.message
    assert events == []


def test_click_target_uses_vision_when_template_file_is_missing(tmp_path):
    events: list[tuple[str, object]] = []

    class FakePyAutoGUI:
        def locateCenterOnScreen(self, path: str, confidence: float = 0.9):
            return None

        def click(self, x: int, y: int) -> None:
            events.append(("click", (x, y)))

    result = click_target(
        "league_confirm_button",
        click_targets={
            "league_confirm_button": {
                "display_name": "Boton Confirmar de League of Legends",
                "template_paths": ("missing.png",),
                "vision_prompt": "Boton CONFIRMAR de League of Legends.",
            }
        },
        pyautogui_module=FakePyAutoGUI(),
        project_root=tmp_path,
        encoded_screen_provider=lambda: "encoded-screen",
        vision_locator=lambda target_name, target_description, encoded_image: {
            "found": True,
            "x": 640,
            "y": 420,
            "confidence": 0.94,
            "reason": "Boton visible.",
            "model_name": "qwen3-vl:30b",
        },
    )

    assert result.success is True
    assert events == [("click", (640, 420))]
    assert "qwen3-vl:30b" in result.message


def test_click_target_falls_back_when_confidence_is_not_supported(tmp_path):
    template_file = tmp_path / "league_play_button.png"
    template_file.write_bytes(b"fake-png")
    events: list[tuple[str, object]] = []

    class Match:
        x = 100
        y = 120

    class FakePyAutoGUI:
        def locateCenterOnScreen(self, path: str, confidence=None):
            events.append(("locate", confidence))
            if confidence is not None:
                raise TypeError("confidence unsupported")
            return Match()

        def click(self, x: int, y: int) -> None:
            events.append(("click", (x, y)))

    result = click_target(
        "league_play_button",
        click_targets={
            "league_play_button": {
                "display_name": "Boton Jugar de League of Legends",
                "template_paths": ("league_play_button.png",),
            }
        },
        pyautogui_module=FakePyAutoGUI(),
        project_root=tmp_path,
    )

    assert result.success is True
    assert events == [("locate", 0.9), ("locate", None), ("click", (100, 120))]


def test_execute_voice_action_clicks_target_with_stubbed_pyautogui(tmp_path):
    template_file = tmp_path / "league_play_button.png"
    template_file.write_bytes(b"fake-png")
    events: list[tuple[str, object]] = []

    class Match:
        x = 512
        y = 384

    class FakePyAutoGUI:
        def locateCenterOnScreen(self, path: str, confidence: float = 0.9):
            events.append(("locate", Path(path).name))
            return Match()

        def click(self, x: int, y: int) -> None:
            events.append(("click", (x, y)))

    plan = VoiceActionPlan(action="click_target", parameters={"target": "league_play_button"})
    result = click_target(
        "league_play_button",
        click_targets={
            "league_play_button": {
                "display_name": "Boton Jugar de League of Legends",
                "template_paths": ("league_play_button.png",),
            }
        },
        pyautogui_module=FakePyAutoGUI(),
        project_root=tmp_path,
    )

    assert result.success is True
    assert events == [("locate", "league_play_button.png"), ("click", (512, 384))]

    result = execute_voice_action(
        plan,
        pyautogui_module=FakePyAutoGUI(),
    )

    assert result.success is False
    assert "No he podido localizar" in result.message or "No he encontrado" in result.message


def test_build_status_message_keeps_only_first_sentence():
    message = (
        "No he podido cerrar chrome porque Windows ha devuelto acceso denegado. "
        "Ejecuta el asistente con los mismos permisos que la aplicacion o cierrala manualmente."
    )

    assert build_status_message(message) == (
        "No he podido cerrar chrome porque Windows ha devuelto acceso denegado."
    )


def test_build_status_message_compacts_multiline_text():
    message = "ERROR: el proceso no se pudo terminar.\nMotivo: Acceso denegado."

    assert build_status_message(message) == "ERROR: el proceso no se pudo terminar."


def test_build_channel_button_label_uses_short_labels():
    assert build_channel_button_label(channel_open=False) == "Hablar"
    assert build_channel_button_label(channel_open=True) == "Apagar"


def test_should_ignore_global_space_shortcut_inside_text_inputs():
    class FakeWidget:
        def __init__(self, widget_class: str) -> None:
            self.widget_class = widget_class

        def winfo_class(self) -> str:
            return self.widget_class

    assert should_ignore_global_space_shortcut(FakeWidget("TEntry")) is True
    assert should_ignore_global_space_shortcut(FakeWidget("Text")) is True
    assert should_ignore_global_space_shortcut(FakeWidget("TFrame")) is False
    assert should_ignore_global_space_shortcut(None) is False


def test_is_process_running_detects_process_from_powershell_output():
    class FakeCompletedProcess:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_process_query_runner(command, capture_output=True, text=True, check=False):
        return FakeCompletedProcess(returncode=0, stdout="1234\n")

    assert is_process_running("chrome.exe", process_query_runner=fake_process_query_runner) is True


def test_close_application_uses_taskkill_for_allowed_process():
    commands: list[list[str]] = []
    queries: list[list[str]] = []

    class FakeCompletedProcess:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_command_runner(command, capture_output=True, text=True, check=False):
        commands.append(command)
        return FakeCompletedProcess(returncode=0)

    query_results = iter(["1234\n", ""])

    def fake_process_query_runner(command, capture_output=True, text=True, check=False):
        queries.append(command)
        return FakeCompletedProcess(returncode=0, stdout=next(query_results))

    result = close_application(
        "chrome",
        command_runner=fake_command_runner,
        process_query_runner=fake_process_query_runner,
    )

    assert result.success is True
    assert commands == [["taskkill", "/IM", "chrome.exe", "/T", "/F"]]
    assert len(queries) == 2


def test_close_application_supports_league_client_process():
    commands: list[list[str]] = []

    class FakeCompletedProcess:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_command_runner(command, capture_output=True, text=True, check=False):
        commands.append(command)
        return FakeCompletedProcess(returncode=0)

    query_results = iter(["1234\n", ""])

    def fake_process_query_runner(command, capture_output=True, text=True, check=False):
        return FakeCompletedProcess(returncode=0, stdout=next(query_results))

    result = close_application(
        "league_of_legends",
        command_runner=fake_command_runner,
        process_query_runner=fake_process_query_runner,
    )

    assert result.success is True
    assert commands == [["taskkill", "/IM", "LeagueClientUx.exe", "/T", "/F"]]


def test_close_application_supports_riot_client_process_for_league_flow():
    commands: list[list[str]] = []

    class FakeCompletedProcess:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_command_runner(command, capture_output=True, text=True, check=False):
        commands.append(command)
        return FakeCompletedProcess(returncode=0)

    process_outputs = {
        "LeagueClientUx": iter(["", ""]),
        "LeagueClient": iter(["", ""]),
        "League of Legends": iter(["", ""]),
        "RiotClientUx": iter(["1234\n", ""]),
    }

    def fake_process_query_runner(command, capture_output=True, text=True, check=False):
        powershell_command = command[3]
        for process_base_name, output_iter in process_outputs.items():
            if f"Name '{process_base_name}'" in powershell_command:
                return FakeCompletedProcess(returncode=0, stdout=next(output_iter))
        return FakeCompletedProcess(returncode=0, stdout="")

    result = close_application(
        "league_of_legends",
        command_runner=fake_command_runner,
        process_query_runner=fake_process_query_runner,
    )

    assert result.success is True
    assert commands == [["taskkill", "/IM", "RiotClientUx.exe", "/T", "/F"]]


def test_close_application_accepts_taskkill_noise_when_process_has_closed():
    class FakeCompletedProcess:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    query_results = iter(["1234\n", ""])

    def fake_command_runner(command, capture_output=True, text=True, check=False):
        return FakeCompletedProcess(
            returncode=128,
            stderr="ERROR: el proceso con PID 19660 no se pudo terminar.\nMotivo: Acceso denegado.",
        )

    def fake_process_query_runner(command, capture_output=True, text=True, check=False):
        return FakeCompletedProcess(returncode=0, stdout=next(query_results))

    result = close_application(
        "chrome",
        command_runner=fake_command_runner,
        process_query_runner=fake_process_query_runner,
    )

    assert result.success is True
    assert result.message == "He cerrado chrome."


def test_close_application_reports_permission_issue_when_process_still_running():
    class FakeCompletedProcess:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_command_runner(command, capture_output=True, text=True, check=False):
        return FakeCompletedProcess(
            returncode=128,
            stderr="ERROR: el proceso con PID 19660 no se pudo terminar.\nMotivo: Acceso denegado.",
        )

    def fake_process_query_runner(command, capture_output=True, text=True, check=False):
        return FakeCompletedProcess(returncode=0, stdout="1234\n")

    result = close_application(
        "chrome",
        command_runner=fake_command_runner,
        process_query_runner=fake_process_query_runner,
    )

    assert result.success is False
    assert "acceso denegado" in result.message.lower()


def test_execute_voice_action_closes_application_with_stubbed_runner():
    commands: list[list[str]] = []

    class FakeCompletedProcess:
        def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def fake_command_runner(command, capture_output=True, text=True, check=False):
        commands.append(command)
        return FakeCompletedProcess(returncode=0)

    query_results = iter(["1234\n", ""])

    def fake_process_query_runner(command, capture_output=True, text=True, check=False):
        return FakeCompletedProcess(returncode=0, stdout=next(query_results))

    plan = VoiceActionPlan(action="close_application", parameters={"application": "chrome"})
    result = execute_voice_action(
        plan,
        command_runner=fake_command_runner,
        process_query_runner=fake_process_query_runner,
    )

    assert result.success is True
    assert commands == [["taskkill", "/IM", "chrome.exe", "/T", "/F"]]


def test_process_voice_transcript_requires_explicit_confirmation(monkeypatch):
    pending_plan = VoiceActionPlan(
        action="trash_path",
        parameters={"path": "C:\\Users\\demo\\Downloads\\draft.txt"},
        requires_confirmation=True,
        confirmation_prompt="Confirma.",
    )

    monkeypatch.setattr(
        session_orchestration,
        "execute_voice_action",
        lambda plan: session_orchestration.VoiceExecutionResult(
            success=True,
            message=f"Executed {plan.action}",
            action=plan.action,
        ),
    )

    result, next_pending = session_orchestration.process_voice_transcript(
        "confirmar",
        pending_plan=pending_plan,
    )

    assert result.message == "Executed trash_path"
    assert next_pending is None


def test_trash_path_rejects_repo_paths():
    protected_file = ROOT / "README.md"

    result = trash_path(str(protected_file), trash_sender=lambda value: value)

    assert result.success is False
    assert "protegida" in result.message


def test_is_protected_path_allows_external_temp_file(tmp_path):
    external_file = tmp_path / "voice-command.txt"
    external_file.write_text("demo", encoding="utf-8")

    assert is_protected_path(external_file) is False


def test_write_pcm_frames_to_wav_creates_a_valid_file(tmp_path):
    output_path = tmp_path / "voice.wav"
    path = write_pcm_frames_to_wav([b"\x00\x00" * 200], output_path)

    assert path.exists()
    assert path.read_bytes()[:4] == b"RIFF"


def test_load_wav_audio_for_whisper_returns_pcm_array(tmp_path):
    output_path = tmp_path / "voice.wav"
    path = write_pcm_frames_to_wav([b"\x01\x00" * 200], output_path)

    audio_input = load_wav_audio_for_whisper(path)

    assert audio_input["sampling_rate"] == 16000
    assert len(audio_input["array"]) == 200


def test_transcribe_audio_file_sends_waveform_dict_to_pipeline(tmp_path):
    output_path = tmp_path / "voice.wav"
    path = write_pcm_frames_to_wav([b"\x01\x00" * 200], output_path)
    captured_input = {}

    def fake_pipeline_builder(model_name: str):
        def fake_pipeline(audio_input):
            captured_input["value"] = audio_input
            return {"text": "hola desde whisper"}

        return fake_pipeline

    transcript = transcribe_audio_file(path, pipeline_builder=fake_pipeline_builder)

    assert transcript == "hola desde whisper"
    assert isinstance(captured_input["value"], dict)
    assert captured_input["value"]["sampling_rate"] == 16000


def test_build_whisper_pipeline_forces_spanish_transcription():
    captured_kwargs = {}

    def fake_pipeline_factory(task, **kwargs):
        captured_kwargs["task"] = task
        captured_kwargs.update(kwargs)
        return object()

    build_whisper_pipeline(pipeline_factory=fake_pipeline_factory)

    assert captured_kwargs["task"] == "automatic-speech-recognition"
    assert captured_kwargs["generate_kwargs"]["language"] == "spanish"
    assert captured_kwargs["generate_kwargs"]["task"] == "transcribe"


def test_resolve_windows_speech_shell_uses_powershell_exe_first():
    shell_path = resolve_windows_speech_shell(
        shell_finder=lambda name: "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        if name == "powershell.exe"
        else None
    )

    assert shell_path.endswith("powershell.exe")


def test_clean_text_for_speech_collapses_whitespace_and_truncates():
    text = clean_text_for_speech("Hola\n\nmundo   desde   la interfaz local.", max_chars=18)

    assert text == "Hola mundo desd..."


def test_build_windows_speech_command_passes_text_as_argument():
    command = build_windows_speech_command(
        "Hola mundo",
        shell_path="powershell.exe",
    )

    assert command[0] == "powershell.exe"
    assert command[-1] == "Hola mundo"
    assert "System.Speech" in command[3]


def test_local_voice_speaker_stops_previous_process_before_speaking_again():
    events: list[str] = []

    class FakeProcess:
        def __init__(self, name: str) -> None:
            self.name = name
            self.terminated = False

        def poll(self):
            return None if not self.terminated else 0

        def terminate(self) -> None:
            self.terminated = True
            events.append(f"terminate:{self.name}")

        def wait(self, timeout: float = 1) -> int:
            events.append(f"wait:{self.name}")
            return 0

        def kill(self) -> None:
            events.append(f"kill:{self.name}")

    created_processes: list[FakeProcess] = []

    def fake_launcher(text: str, shell_finder=None):
        process = FakeProcess(text)
        created_processes.append(process)
        events.append(f"launch:{text}")
        return process

    speaker = LocalVoiceSpeaker(
        speech_launcher=fake_launcher,
        shell_finder=lambda name: "powershell.exe",
    )

    speaker.speak("primer mensaje")
    speaker.speak("segundo mensaje")

    assert events == [
        "launch:primer mensaje",
        "terminate:primer mensaje",
        "wait:primer mensaje",
        "launch:segundo mensaje",
    ]
    assert created_processes[-1].name == "segundo mensaje"


def test_voice_desktop_controller_processes_recorded_audio(tmp_path):
    events: list[str] = []

    class FakeRecorder:
        def start(self) -> None:
            events.append("start")

        def stop(self) -> Path:
            events.append("stop")
            return tmp_path / "recorded.wav"

    controller = VoiceDesktopController(
        recorder_factory=FakeRecorder,
        transcriber=lambda audio_path: f"transcript from {Path(audio_path).name}",
        transcript_processor=lambda transcript, pending_plan=None: (
            session_orchestration.VoiceExecutionResult(
                success=True,
                message=f"processed {transcript}",
                action="answer",
            ),
            pending_plan,
        ),
        exit_checker=lambda transcript: False,
    )

    assert controller.start_recording() == "Escuchando."
    turn = controller.stop_recording_and_process()

    assert events == ["start", "stop"]
    assert turn.transcript == "transcript from recorded.wav"
    assert turn.assistant_message == "processed transcript from recorded.wav"


def test_voice_desktop_controller_opens_and_closes_channel():
    events: list[str] = []

    class FakeChannel:
        def start(self) -> None:
            events.append("start")

        def stop(self) -> None:
            events.append("stop")

    controller = VoiceDesktopController(
        recorder_factory=lambda: None,
        channel_factory=FakeChannel,
        transcriber=lambda audio_path: "unused",
        transcript_processor=lambda transcript, pending_plan=None: (
            session_orchestration.VoiceExecutionResult(
                success=True,
                message="unused",
                action="answer",
            ),
            pending_plan,
        ),
        exit_checker=lambda transcript: False,
    )

    assert controller.open_channel() == "Canal abierto. Escuchando."
    assert controller.close_channel() == "Canal cerrado."
    assert events == ["start", "stop"]


def test_voice_desktop_controller_listens_once_and_processes_channel_audio(tmp_path):
    events: list[str] = []

    class FakeChannel:
        def start(self) -> None:
            events.append("start")

        def stop(self) -> None:
            events.append("stop")

        def capture_next_utterance(self):
            events.append("capture")
            return tmp_path / "voice_channel.wav"

    controller = VoiceDesktopController(
        recorder_factory=lambda: None,
        channel_factory=FakeChannel,
        transcriber=lambda audio_path: f"transcript from {Path(audio_path).name}",
        transcript_processor=lambda transcript, pending_plan=None: (
            session_orchestration.VoiceExecutionResult(
                success=True,
                message=f"processed {transcript}",
                action="answer",
            ),
            pending_plan,
        ),
        exit_checker=lambda transcript: False,
    )

    controller.open_channel()
    turn = controller.listen_once_and_process()

    assert turn is not None
    assert turn.transcript == "transcript from voice_channel.wav"
    assert turn.assistant_message == "processed transcript from voice_channel.wav"
    assert events == ["start", "capture"]


def test_voice_desktop_controller_marks_exit_requested():
    controller = VoiceDesktopController(
        recorder_factory=lambda: None,
        transcriber=lambda audio_path: "salir",
        transcript_processor=lambda transcript, pending_plan=None: (
            session_orchestration.VoiceExecutionResult(
                success=True,
                message="unused",
                action="answer",
            ),
            pending_plan,
        ),
        exit_checker=lambda transcript: transcript == "salir",
    )

    turn = controller.submit_transcript("salir")

    assert turn.exit_requested is True
    assert turn.assistant_message == "Sesion cerrada."
