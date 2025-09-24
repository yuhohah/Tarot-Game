from .Deck import Deck


class DeckManager:
    def __init__(self):
        self.deck = Deck.get_deck()
        self.shuffle_deck()

    def shuffle_deck(self):
        """Embaralha o deck de cartas"""
        Deck.deck_suffle(self.deck)

    def get_card(self):
        """Retorna uma carta do deck"""
        return Deck.get_card(self.deck)

    def get_deck(self):
        """Retorna o deck completo"""
        return self.deck