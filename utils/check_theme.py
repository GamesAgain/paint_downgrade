
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

def check_system_theme():
    scheme = QGuiApplication.styleHints().colorScheme()
    if scheme == Qt.ColorScheme.Dark:
        return "dark"
    else:
        return "light"
