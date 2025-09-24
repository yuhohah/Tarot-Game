# Permite que o diretório models seja tratado como um pacote Python
from .deck_manager import DeckManager
from .Deck import Deck

__all__ = ['DeckManager', 'Deck']