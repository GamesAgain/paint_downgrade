from .check_theme import check_system_theme

def load_icon_path():
    apply_theme = check_system_theme()
    return "icons/" + apply_theme + "/"