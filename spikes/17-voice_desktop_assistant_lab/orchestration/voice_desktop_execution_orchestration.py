# --- DEPENDENCIAS ---
import subprocess
import webbrowser
from pathlib import Path

from config.voice_desktop_config import PROJECT_ROOT
from config.voice_desktop_config import PROTECTED_PATH_FRAGMENTS
from data.voice_command_catalog import ALLOWED_APPLICATIONS
from data.voice_command_catalog import CLOSEABLE_APPLICATION_PROCESSES
from models.voice_desktop_entities import VoiceActionPlan
from models.voice_desktop_entities import VoiceExecutionResult


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
        raise RuntimeError("Install pyautogui to automate keyboard actions.") from exc

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
    process_launcher=subprocess.Popen,
) -> VoiceExecutionResult:
    command = app_catalog.get(application_name)
    if not command:
        return VoiceExecutionResult(
            success=False,
            message=f"La aplicacion {application_name} no esta permitida.",
            action="open_application",
        )

    process_launcher(command)
    return VoiceExecutionResult(
        success=True,
        message=f"He abierto {application_name}.",
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

    if plan.action == "press_hotkey":
        return press_hotkey(
            keys=list(plan.parameters.get("keys", [])),
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
