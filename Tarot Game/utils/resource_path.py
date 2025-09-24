import os
import sys

def resource_path(relative_path):
    """Obter o caminho absoluto para recursos, considerando o PyInstaller."""
    try:
        # Quando executado como um executável
        base_path = sys._MEIPASS
    except AttributeError:
        # Quando executado como um script Python
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


    return os.path.join(base_path, relative_path)