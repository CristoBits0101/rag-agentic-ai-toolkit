# --- DEPENDENCIAS ---
ALLOWED_ACTIONS = (
    "answer",
    "click_mouse",
    "click_target",
    "close_application",
    "move_mouse",
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
    "league_of_legends": ["cmd", "/c", "start", "", "riotclient://"],
    "notepad": ["notepad"],
    "paint": ["mspaint"],
    "riot_client": ["cmd", "/c", "start", "", "riotclient://"],
}

CLOSEABLE_APPLICATION_PROCESSES = {
    "calculator": ["calc.exe", "CalculatorApp.exe"],
    "chrome": ["chrome.exe"],
    "league_of_legends": [
        "LeagueClientUx.exe",
        "LeagueClient.exe",
        "League of Legends.exe",
        "RiotClientUx.exe",
        "RiotClientServices.exe",
    ],
    "notepad": ["notepad.exe"],
    "paint": ["mspaint.exe"],
    "riot_client": ["RiotClientUx.exe", "RiotClientServices.exe"],
}

APPLICATION_ALIASES = {
    "bloc de notas": "notepad",
    "calculadora": "calculator",
    "calculator": "calculator",
    "chrome": "chrome",
    "explorador": "explorer",
    "explorer": "explorer",
    "google chrome": "chrome",
    "league": "league_of_legends",
    "league of legends": "league_of_legends",
    "lol": "league_of_legends",
    "notepad": "notepad",
    "paint": "paint",
    "riot": "riot_client",
    "riot client": "riot_client",
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

ALLOWED_CLICK_TARGETS = {
    "riot_lol_icon": {
        "display_name": "Icono de League of Legends en Riot Client",
        "template_paths": (
            "spikes/17-voice_assistant/assets/riot_lol_icon.png",
        ),
        "vision_prompt": (
            "El icono gris oscuro de League of Legends con el simbolo dorado de LoL "
            "en la pantalla principal de Riot Client."
        ),
    },
    "riot_play_button": {
        "display_name": "Boton Jugar de Riot Client",
        "template_paths": (
            "spikes/17-voice_assistant/assets/riot_play_button.png",
        ),
        "vision_prompt": (
            "El boton grande amarillo o dorado con el texto Jugar y el icono triangular "
            "de reproducir en Riot Client."
        ),
    },
    "league_play_button": {
        "display_name": "Boton Jugar de League of Legends",
        "template_paths": (
            "spikes/17-voice_assistant/assets/league_play_button.png",
        ),
        "vision_prompt": "El boton JUGAR azul con borde dorado del cliente de League of Legends o Riot Client.",
    },
    "league_ranked_solo_duo_option": {
        "display_name": "Opcion Clasificatoria Solo/Duo de League of Legends",
        "template_paths": (
            "spikes/17-voice_assistant/assets/league_ranked_solo_duo_option.png",
        ),
        "vision_prompt": "La opcion CLASIFICATORIA SOLO/DUO del menu de modos de juego de League of Legends.",
    },
    "league_confirm_button": {
        "display_name": "Boton Confirmar de League of Legends",
        "template_paths": (
            "spikes/17-voice_assistant/assets/league_confirm_button.png",
        ),
        "vision_prompt": "El boton CONFIRMAR azul en la parte derecha o inferior del cliente de League of Legends.",
    },
    "league_find_match_button": {
        "display_name": "Boton Encontrar Partida de League of Legends",
        "template_paths": (
            "spikes/17-voice_assistant/assets/league_find_match_button.png",
        ),
        "vision_prompt": "El boton ENCONTRAR PARTIDA azul brillante del cliente de League of Legends.",
    },
}

CLICK_TARGET_ALIASES = {
    "boton confirmar": "league_confirm_button",
    "boton jugar riot": "riot_play_button",
    "dale a jugar en league": "league_play_button",
    "dale a jugar en league of legends": "league_play_button",
    "dale a jugar en leaguea of legends": "league_play_button",
    "dale a jugar en lol": "league_play_button",
    "buscar partida": "league_find_match_button",
    "busca partida": "league_find_match_button",
    "boton jugar league": "league_play_button",
    "boton jugar league of legends": "league_play_button",
    "boton jugar lol": "league_play_button",
    "clasificatoria duo": "league_ranked_solo_duo_option",
    "clasificatoria solo duo": "league_ranked_solo_duo_option",
    "clasificatoria solo/duo": "league_ranked_solo_duo_option",
    "confirma": "league_confirm_button",
    "confirma la cola": "league_confirm_button",
    "confirmar": "league_confirm_button",
    "confirmar cola": "league_confirm_button",
    "darle a jugar en league": "league_play_button",
    "darle a jugar en league of legends": "league_play_button",
    "darle a jugar en leaguea of legends": "league_play_button",
    "darle a jugar en lol": "league_play_button",
    "dale a confirmar": "league_confirm_button",
    "encontrar partida": "league_find_match_button",
    "icono lol": "riot_lol_icon",
    "jugar en league": "league_play_button",
    "jugar en league of legends": "league_play_button",
    "jugar en leaguea of legends": "league_play_button",
    "jugar en lol": "league_play_button",
    "modo clasificatoria duo": "league_ranked_solo_duo_option",
    "modo clasificatoria solo duo": "league_ranked_solo_duo_option",
    "pon clasificatoria duo": "league_ranked_solo_duo_option",
    "pulsa confirmar": "league_confirm_button",
    "pulsa encontrar partida": "league_find_match_button",
    "pulsa clasificatoria duo": "league_ranked_solo_duo_option",
    "pulsa clasificatoria solo duo": "league_ranked_solo_duo_option",
    "solo duo": "league_ranked_solo_duo_option",
}

APPLICATION_OPEN_WORKFLOWS = {
    "league_of_legends": (
        "riot_lol_icon",
        "riot_play_button",
    ),
}
