# --- DEPENDENCIAS ---
ALLOWED_ACTIONS = (
    "answer",
    "close_application",
    "no_op",
    "open_application",
    "open_url",
    "press_hotkey",
    "trash_path",
    "type_text",
)

ALLOWED_APPLICATIONS = {
    "calculator": ["calc"],
    "chrome": ["cmd", "/c", "start", "", "chrome"],
    "explorer": ["explorer"],
    "notepad": ["notepad"],
    "paint": ["mspaint"],
}

CLOSEABLE_APPLICATION_PROCESSES = {
    "calculator": ["calc.exe", "CalculatorApp.exe"],
    "chrome": ["chrome.exe"],
    "notepad": ["notepad.exe"],
    "paint": ["mspaint.exe"],
}

APPLICATION_ALIASES = {
    "bloc de notas": "notepad",
    "calculadora": "calculator",
    "calculator": "calculator",
    "chrome": "chrome",
    "explorador": "explorer",
    "explorer": "explorer",
    "google chrome": "chrome",
    "notepad": "notepad",
    "paint": "paint",
}

KNOWN_URLS = {
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "google": "https://www.google.com",
    "spotify": "https://open.spotify.com",
    "youtube": "https://www.youtube.com",
}

HOTKEY_ALIASES = {
    "alt": "alt",
    "borrar": "delete",
    "control": "ctrl",
    "ctrl": "ctrl",
    "delete": "delete",
    "enter": "enter",
    "escape": "esc",
    "esc": "esc",
    "intro": "enter",
    "mayus": "shift",
    "shift": "shift",
    "suprimir": "delete",
    "tab": "tab",
    "tecla windows": "win",
    "windows": "win",
    "win": "win",
}
