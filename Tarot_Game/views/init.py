# Permite que o diretório views seja tratado como um pacote Python
from .deck_view import DeckView
from .game_view import GameView
from .main_view import Application

__all__ = ['Application', 'GameView', 'DeckView']