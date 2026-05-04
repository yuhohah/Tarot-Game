from typing import List, Any
from utils.QNRG import QNRG

class Shuffler:
    """
    Shuffles a deck (list) using true random bytes from your QNRG API.
    Uses Fisher‑Yates with rejection sampling to guarantee uniform distribution.
    """

    def __init__(self):
        """
        Args:
            qnrg: An instance of your QNRG class (with _fetch_from_api method).
        """
        self.qnrg = QNRG()
        self._byte_cache = []   # holds raw bytes (0‑255)
        self._cache_pos = 0

    def _refill_cache(self, num_bytes: int = 100):
        """Fetch fresh random bytes from the qnrg and append to cache."""
        new_bytes = self.qnrg._fetch_from_api(amount=num_bytes, bits_per_block=8)
        if new_bytes is None:
            raise ConnectionError("Failed to retrieve quantum random numbers")
        self._byte_cache.extend(new_bytes)

    def _get_number(self) -> int:
        """Return one random byte (0‑255) from the cache, refilling if empty."""
        if self._cache_pos >= len(self._byte_cache):
            self._refill_cache()
            self._cache_pos = 0
        number = self._byte_cache[self._cache_pos]
        self._cache_pos += 1
        return number

    def _randint(self, a: int, b: int) -> int:
        """
        Return a uniform integer N with a <= N <= b, using rejection sampling
        on the raw random bytes.
        """
        range_len = b - a + 1
        # Largest multiple of range_len that fits in 0..255
        max_valid = 256 - (256 % range_len)

        while True:
            number = self._get_number()
            if number < max_valid:
                return a + (number % range_len)

    def shuffle(self, deck: List[Any]):
        """
        Shuffle the deck in place using quantum random numbers.

        Args:
            deck: Your tarot deck (list of cards or any objects).

        Returns:
            The shuffled deck (same list, modified in place).
        """
        n = len(deck)
        for i in range(n - 1, 0, -1):
            j = self._randint(0, i)
            deck[i], deck[j] = deck[j], deck[i]
        

    def shuffled_copy(self, deck: List[Any]) -> List[Any]:
        """Return a new shuffled copy of the deck."""
        import copy
        new_deck = copy.deepcopy(deck)
        self.shuffle(new_deck)
        return new_deck