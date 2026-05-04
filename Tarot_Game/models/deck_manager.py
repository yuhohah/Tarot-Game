from .deck import Deck
from utils.deck_state import DeckState

class DeckManager:
    def __init__(self):
        saved_state = DeckState.load_last_state()
        reference_deck = {card["sequence"]: card for card in Deck.get_deck()}
        
        if saved_state:
            # Reconstruct deck and drawn cards from sequence IDs
            self.deck = []
            for item in saved_state.get("deck", []):
                if isinstance(item, dict):
                    self.deck.append(item)
                else:
                    self.deck.append(reference_deck[item])
            
            self.drawn_cards = []
            for item in saved_state.get("drawn_cards", []):
                if isinstance(item, (tuple, list)):
                    if isinstance(item[0], dict):
                        self.drawn_cards.append(tuple(item))
                    else:
                        self.drawn_cards.append((reference_deck[item[0]], item[1]))
                else:
                    self.drawn_cards.append(item)
        else:
            self.deck = Deck.get_deck()
            self.drawn_cards = []
            self.shuffle_deck()

    def shuffle_deck(self):
        """Embaralha o deck de cartas"""
        # Put drawn cards back at the end of the deck
        if hasattr(self, 'drawn_cards') and self.drawn_cards:
            # Extract just the card dict from the tuple if it's stored as (card, rev) or [card, rev]
            cards_to_return = [drawn[0] for drawn in self.drawn_cards] if isinstance(self.drawn_cards[0], (tuple, list)) else self.drawn_cards
            self.deck.extend(cards_to_return)
            self.drawn_cards = []
            
        try:
            Deck.deck_suffle(self.deck)
        except Exception as e:
            from tkinter import messagebox
            import random
            messagebox.showerror("Erro na API Quântica", f"Falha na conexão: {e}\n\nUsando embaralhador padrão do Python.")
            random.shuffle(self.deck)
            
        DeckState.save_state(self.deck, self.drawn_cards)

    def get_card(self):
        """Retorna uma carta do deck"""
        card = Deck.get_card(self.deck)
        if card:
            self.drawn_cards.append(card)
            DeckState.save_state(self.deck, self.drawn_cards)
        return card

    def get_deck(self):
        """Retorna o deck completo"""
        return self.deck