import json
import os

class DeckState:
    """Utility class to save and load the current order of the deck."""

    @staticmethod
    def load_history(filename: str = "tarot_deck_state.json") -> list:
        # Keeping this for backwards compatibility if needed, but not used by save_state anymore
        pass

    @staticmethod
    def save_state(deck: list, drawn_cards: list, filename: str = "tarot_deck_state.json") -> None:
        """
        Saves the current state of the deck to a JSON file.
        Only saves the card 'sequence' number.
        """
        # Convert deck to IDs and reversed state: [seq, is_reversed]
        deck_ids = []
        for card in deck:
            if isinstance(card, dict):
                deck_ids.append([card["sequence"], 1 if card.get("is_reversed") else 0])
            else:
                deck_ids.append(card)
        
        # Convert drawn cards to [seq, rev]
        drawn_ids = []
        for drawn in drawn_cards:
            if isinstance(drawn, (tuple, list)):
                card = drawn[0]
                rev = drawn[1]
                seq = card["sequence"] if isinstance(card, dict) else card
                drawn_ids.append([seq, rev])
            else:
                drawn_ids.append(drawn)
                
        state = {
            "deck": deck_ids,
            "drawn_cards": drawn_ids
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_last_state(filename: str = "tarot_deck_state.json") -> dict:
        """
        Loads the state from the JSON file. 
        Handles migration if the file is an array of states.
        """
        if not os.path.exists(filename):
            return None
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    # If it's a history array of states, return the last one
                    if data and isinstance(data[-1], dict) and "deck" in data[-1]:
                        return data[-1]
                    # If it's the very old list of raw cards
                    elif data and isinstance(data[0], dict) and "deck" not in data[0]:
                        return {"deck": data, "drawn_cards": []}
                    return data[-1] if data else None
                elif isinstance(data, dict):
                    return data
        except Exception:
            return None
        return None

    @staticmethod
    def load_state(filename: str = "tarot_deck_state.json") -> dict:
        return DeckState.load_last_state(filename)
