# --- DEPENDENCIAS ---
import subprocess
import time
import webbrowser
from pathlib import Path

from config.voice_desktop_config import APPLICATION_STARTUP_DELAY_SECONDS
from config.voice_desktop_config import CLICK_MATCH_CONFIDENCE
from config.voice_desktop_config import CLICK_TARGET_RETRY_ATTEMPTS
from config.voice_desktop_config import CLICK_TARGET_RETRY_DELAY_SECONDS
from config.voice_desktop_config import PROJECT_ROOT
from config.voice_desktop_config import PROTECTED_PATH_FRAGMENTS
from data.voice_command_catalog import ALLOWED_CLICK_TARGETS
from data.voice_command_catalog import ALLOWED_APPLICATIONS
from data.voice_command_catalog import APPLICATION_OPEN_WORKFLOWS
from data.voice_command_catalog import CLOSEABLE_APPLICATION_PROCESSES
from models.voice_desktop_entities import VoiceActionPlan
from models.voice_desktop_entities import VoiceExecutionResult
from models.voice_screen_vision_gateway import encode_image_to_base64
from models.voice_screen_vision_gateway import locate_click_target_with_vision


def load_send2trash():
    try:
        from send2trash import send2trash
    except ImportError as exc:
        raise RuntimeError("Install Send2Trash to send files to the recycle bin.") from exc

    return send2trash


def load_pyautogui():
    try:
        import pyautogui
    except ImportError as exc:
        raise RuntimeError("Install pyautogui to automate keyboard and mouse actions.") from exc

    return pyautogui


def is_protected_path(path_value: str | Path) -> bool:
    path = Path(path_value).expanduser().resolve(strict=False)
    path_text = str(path).lower()
    if path == Path(path.anchor):
        return True

    if any(fragment in path_text for fragment in PROTECTED_PATH_FRAGMENTS):
        return True

    try:
        path.relative_to(PROJECT_ROOT)
        return True
    except ValueError:
        return False


def open_application(
    application_name: str,
    app_catalog: dict[str, list[str]] = ALLOWED_APPLICATIONS,
    open_workflows: dict[str, tuple[str, ...]] = APPLICATION_OPEN_WORKFLOWS,
    process_launcher=subprocess.Popen,
    pyautogui_module=None,
    click_executor=None,
    sleep_fn=time.sleep,
    startup_delay_seconds: float = APPLICATION_STARTUP_DELAY_SECONDS,
    click_retry_attempts: int = CLICK_TARGET_RETRY_ATTEMPTS,
    click_retry_delay_seconds: float = CLICK_TARGET_RETRY_DELAY_SECONDS,
) -> VoiceExecutionResult:
    command = app_catalog.get(application_name)
    if not command:
        return VoiceExecutionResult(
            success=False,
            message=f"La aplicacion {application_name} no esta permitida.",
            action="open_application",
        )

    process_launcher(command)
    workflow_targets = open_workflows.get(application_name, ())
    if not workflow_targets:
        return VoiceExecutionResult(
            success=True,
            message=f"He abierto {application_name}.",
            action="open_application",
        )

    pyautogui_module = pyautogui_module or load_pyautogui()
    click_executor = click_executor or click_target
    if startup_delay_seconds > 0:
        sleep_fn(startup_delay_seconds)

    if application_name == "league_of_legends":
        direct_play_result = click_target_with_retries(
            target_name="riot_play_button",
            click_executor=click_executor,
            pyautogui_module=pyautogui_module,
            sleep_fn=sleep_fn,
            retry_attempts=click_retry_attempts,
            retry_delay_seconds=click_retry_delay_seconds,
        )
        if direct_play_result.success:
            return VoiceExecutionResult(
                success=True,
                message=f"He abierto {application_name} y he completado riot_play_button.",
                action="open_application",
            )

    completed_targets: list[str] = []
    for target_name in workflow_targets:
        result = click_target_with_retries(
            target_name=target_name,
            click_executor=click_executor,
            pyautogui_module=pyautogui_module,
            sleep_fn=sleep_fn,
            retry_attempts=click_retry_attempts,
            retry_delay_seconds=click_retry_delay_seconds,
        )
        if not result.success:
            return VoiceExecutionResult(
                success=False,
                message=(
                    f"He abierto {application_name} pero no he podido completar el paso "
                    f"{target_name}: {result.message}"
                ),
                action="open_application",
            )
        completed_targets.append(target_name)

    return VoiceExecutionResult(
        success=True,
        message=f"He abierto {application_name} y he completado {' -> '.join(completed_targets)}.",
        action="open_application",
    )


def open_url(
    url: str,
    browser_opener=webbrowser.open,
) -> VoiceExecutionResult:
    browser_opener(url)
    return VoiceExecutionResult(
        success=True,
        message=f"He abierto {url}.",
        action="open_url",
    )


def is_process_running(
    process_name: str,
    process_query_runner=subprocess.run,
) -> bool:
    process_base_name = Path(process_name).stem
    result = process_query_runner(
        [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            (
                f"$process = Get-Process -Name '{process_base_name}' -ErrorAction SilentlyContinue | "
                "Select-Object -First 1 -ExpandProperty Id; "
                "if ($null -ne $process) { Write-Output $process }"
            ),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and bool((result.stdout or "").strip())


def close_application(
    application_name: str,
    closeable_processes: dict[str, list[str]] = CLOSEABLE_APPLICATION_PROCESSES,
    command_runner=subprocess.run,
    process_query_runner=subprocess.run,
) -> VoiceExecutionResult:
    process_names = closeable_processes.get(application_name)
    if not process_names:
        return VoiceExecutionResult(
            success=False,
            message=f"La aplicacion {application_name} no se puede cerrar de forma segura.",
            action="close_application",
        )

    found_active_instance = False
    last_error = ""
    access_denied = False
    for process_name in process_names:
        if not is_process_running(process_name, process_query_runner=process_query_runner):
            continue

        found_active_instance = True
        result = command_runner(
            ["taskkill", "/IM", process_name, "/T", "/F"],
            capture_output=True,
            text=True,
            check=False,
        )
        if not is_process_running(process_name, process_query_runner=process_query_runner):
            return VoiceExecutionResult(
                success=True,
                message=f"He cerrado {application_name}.",
                action="close_application",
            )

        last_error = (result.stderr or result.stdout or "").strip()
        normalized_error = last_error.lower()
        if "acceso denegado" in normalized_error or "access is denied" in normalized_error:
            access_denied = True

    if not found_active_instance:
        return VoiceExecutionResult(
            success=False,
            message=f"No he encontrado ninguna instancia activa de {application_name}.",
            action="close_application",
        )

    if access_denied:
        return VoiceExecutionResult(
            success=False,
            message=(
                f"No he podido cerrar {application_name} porque Windows ha devuelto acceso denegado. "
                "Ejecuta el asistente con los mismos permisos que la aplicacion o cierrala manualmente."
            ),
            action="close_application",
        )

    if last_error:
        return VoiceExecutionResult(
            success=False,
            message=f"No he podido cerrar {application_name}: {last_error}",
            action="close_application",
        )

    return VoiceExecutionResult(
        success=False,
        message=f"No he podido cerrar {application_name}.",
        action="close_application",
    )


def type_text(
    text: str,
    pyautogui_module=None,
) -> VoiceExecutionResult:
    pyautogui_module = pyautogui_module or load_pyautogui()
    pyautogui_module.write(text, interval=0.01)
    return VoiceExecutionResult(
        success=True,
        message="He escrito el texto solicitado.",
        action="type_text",
    )


def press_hotkey(
    keys: list[str],
    pyautogui_module=None,
) -> VoiceExecutionResult:
    pyautogui_module = pyautogui_module or load_pyautogui()
    pyautogui_module.hotkey(*keys)
    return VoiceExecutionResult(
        success=True,
        message=f"He pulsado el atajo {' + '.join(keys)}.",
        action="press_hotkey",
    )


def move_mouse(
    x: int,
    y: int,
    pyautogui_module=None,
) -> VoiceExecutionResult:
    pyautogui_module = pyautogui_module or load_pyautogui()
    pyautogui_module.moveTo(x, y, duration=0.2)
    return VoiceExecutionResult(
        success=True,
        message=f"He movido el raton a {x}, {y}.",
        action="move_mouse",
    )


def click_mouse(
    button: str = "left",
    x: int | None = None,
    y: int | None = None,
    pyautogui_module=None,
) -> VoiceExecutionResult:
    pyautogui_module = pyautogui_module or load_pyautogui()
    if x is None or y is None:
        pyautogui_module.click(button=button)
        return VoiceExecutionResult(
            success=True,
            message=f"He hecho click {button} con el raton.",
            action="click_mouse",
        )

    pyautogui_module.click(x=x, y=y, button=button)
    return VoiceExecutionResult(
        success=True,
        message=f"He hecho click {button} en {x}, {y}.",
        action="click_mouse",
    )


def capture_screen_base64(pyautogui_module) -> str:
    screenshot = pyautogui_module.screenshot()
    return encode_image_to_base64(screenshot)


def click_target_with_retries(
    target_name: str,
    click_executor=None,
    pyautogui_module=None,
    sleep_fn=time.sleep,
    retry_attempts: int = CLICK_TARGET_RETRY_ATTEMPTS,
    retry_delay_seconds: float = CLICK_TARGET_RETRY_DELAY_SECONDS,
) -> VoiceExecutionResult:
    click_executor = click_executor or click_target
    last_result = VoiceExecutionResult(
        success=False,
        message=f"No he podido pulsar {target_name}.",
        action="click_target",
    )
    for attempt_index in range(retry_attempts):
        last_result = click_executor(
            target_name,
            pyautogui_module=pyautogui_module,
        )
        if last_result.success:
            return last_result
        if attempt_index < retry_attempts - 1 and retry_delay_seconds > 0:
            sleep_fn(retry_delay_seconds)
    return last_result


def click_target(
    target_name: str,
    click_targets: dict[str, dict] = ALLOWED_CLICK_TARGETS,
    pyautogui_module=None,
    project_root: Path = PROJECT_ROOT,
    confidence: float = CLICK_MATCH_CONFIDENCE,
    encoded_screen_provider=None,
    vision_locator=locate_click_target_with_vision,
) -> VoiceExecutionResult:
    target_config = click_targets.get(target_name)
    if not target_config:
        return VoiceExecutionResult(
            success=False,
            message=f"El objetivo de click {target_name} no esta permitido.",
            action="click_target",
        )

    target_sequence = tuple(target_config.get("target_sequence", ()))
    if target_sequence:
        last_result = VoiceExecutionResult(
            success=False,
            message=f"No he encontrado {target_config.get('display_name', target_name)} en pantalla.",
            action="click_target",
        )
        for nested_target_name in target_sequence:
            last_result = click_target(
                nested_target_name,
                click_targets=click_targets,
                pyautogui_module=pyautogui_module,
                project_root=project_root,
                confidence=confidence,
                encoded_screen_provider=encoded_screen_provider,
                vision_locator=vision_locator,
            )
            if last_result.success:
                return last_result
        return last_result

    pyautogui_module = pyautogui_module or load_pyautogui()
    template_paths = target_config.get("template_paths", ())
    found_template_file = False
    for template_path in template_paths:
        resolved_path = (project_root / template_path).resolve(strict=False)
        if not resolved_path.exists():
            continue
        found_template_file = True

        try:
            match = pyautogui_module.locateCenterOnScreen(str(resolved_path), confidence=confidence)
        except TypeError:
            match = pyautogui_module.locateCenterOnScreen(str(resolved_path))
        if match is None:
            continue

        pyautogui_module.click(match.x, match.y)
        display_name = target_config.get("display_name", target_name)
        return VoiceExecutionResult(
            success=True,
            message=f"He pulsado {display_name}.",
            action="click_target",
        )

    display_name = target_config.get("display_name", target_name)
    target_description = target_config.get("vision_prompt", display_name)
    encoded_screen_provider = encoded_screen_provider or (lambda: capture_screen_base64(pyautogui_module))
    try:
        prediction = vision_locator(
            target_name=target_name,
            target_description=target_description,
            encoded_image=encoded_screen_provider(),
        )
    except Exception as exc:
        prediction = None
        vision_error = str(exc)
    else:
        vision_error = ""

    if prediction and prediction.get("found"):
        pyautogui_module.click(int(prediction["x"]), int(prediction["y"]))
        return VoiceExecutionResult(
            success=True,
            message=(
                f"He pulsado {display_name} usando vision sobre la pantalla actual con "
                f"{prediction['model_name']}."
            ),
            action="click_target",
        )

    if not found_template_file and vision_error:
        return VoiceExecutionResult(
            success=False,
            message=(
                f"No he podido localizar {display_name} porque no existe plantilla local y la vision ha fallado: "
                f"{vision_error}"
            ),
            action="click_target",
        )

    vision_reason = ""
    if prediction and prediction.get("reason"):
        vision_reason = f" Motivo de vision: {prediction['reason']}"
    return VoiceExecutionResult(
        success=False,
        message=(
            f"No he encontrado {display_name} en pantalla. "
            "Necesito que la ventana este visible y que el objetivo aparezca claramente en la captura."
            f"{vision_reason}"
        ),
        action="click_target",
    )


def trash_path(
    path_value: str,
    trash_sender=None,
) -> VoiceExecutionResult:
    path = Path(path_value).expanduser().resolve(strict=False)
    if not path.exists():
        return VoiceExecutionResult(
            success=False,
            message="La ruta indicada no existe.",
            action="trash_path",
        )

    if is_protected_path(path):
        return VoiceExecutionResult(
            success=False,
            message="No puedo enviar esa ruta a la papelera porque esta protegida.",
            action="trash_path",
        )

    trash_sender = trash_sender or load_send2trash()
    trash_sender(str(path))
    return VoiceExecutionResult(
        success=True,
        message=f"He enviado a la papelera {path}.",
        action="trash_path",
    )


def execute_voice_action(
    plan: VoiceActionPlan,
    app_catalog: dict[str, list[str]] = ALLOWED_APPLICATIONS,
    closeable_processes: dict[str, list[str]] = CLOSEABLE_APPLICATION_PROCESSES,
    process_launcher=subprocess.Popen,
    command_runner=subprocess.run,
    process_query_runner=subprocess.run,
    browser_opener=webbrowser.open,
    pyautogui_module=None,
    trash_sender=None,
) -> VoiceExecutionResult:
    if plan.action in {"answer", "no_op"}:
        return VoiceExecutionResult(
            success=True,
            message=plan.response,
            action=plan.action,
        )

    if plan.action == "open_application":
        return open_application(
            application_name=str(plan.parameters.get("application", "")).strip(),
            app_catalog=app_catalog,
            process_launcher=process_launcher,
            pyautogui_module=pyautogui_module,
        )

    if plan.action == "close_application":
        return close_application(
            application_name=str(plan.parameters.get("application", "")).strip(),
            closeable_processes=closeable_processes,
            command_runner=command_runner,
            process_query_runner=process_query_runner,
        )

    if plan.action == "open_url":
        return open_url(
            url=str(plan.parameters.get("url", "")).strip(),
            browser_opener=browser_opener,
        )

    if plan.action == "type_text":
        return type_text(
            text=str(plan.parameters.get("text", "")),
            pyautogui_module=pyautogui_module,
        )

    if plan.action == "move_mouse":
        return move_mouse(
            x=int(plan.parameters.get("x", 0)),
            y=int(plan.parameters.get("y", 0)),
            pyautogui_module=pyautogui_module,
        )

    if plan.action == "click_mouse":
        return click_mouse(
            button=str(plan.parameters.get("button", "left")),
            x=int(plan.parameters["x"]) if "x" in plan.parameters and "y" in plan.parameters else None,
            y=int(plan.parameters["y"]) if "x" in plan.parameters and "y" in plan.parameters else None,
            pyautogui_module=pyautogui_module,
        )

    if plan.action == "press_hotkey":
        return press_hotkey(
            keys=list(plan.parameters.get("keys", [])),
            pyautogui_module=pyautogui_module,
        )

    if plan.action == "click_target":
        return click_target(
            target_name=str(plan.parameters.get("target", "")).strip(),
            pyautogui_module=pyautogui_module,
        )

    if plan.action == "trash_path":
        return trash_path(
            path_value=str(plan.parameters.get("path", "")).strip(),
            trash_sender=trash_sender,
        )

    return VoiceExecutionResult(
        success=False,
        message=f"La accion {plan.action} no esta soportada.",
        action=plan.action,
    )
