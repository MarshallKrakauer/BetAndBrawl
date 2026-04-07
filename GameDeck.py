from Card import Card
import random


class GameDeck:
    """Represents the shared game box deck from which fighters acquire cards.

    The game deck contains a full set of cards including basic (no-effect) cards,
    charge-effect cards, and cancel cards. Fighters draw from this deck during
    setup to customize their personal decks before a bout.

    Attributes:
        card_list (list[Card]): The shuffled pool of available cards.
    """

    def __init__(self, all_ones_charge=False, num_cancel_cards=6):
        """Initialize a GameDeck with all basic, charge-effect, and cancel cards, then shuffle.

        Args:
            all_ones_charge (bool): If True, all value-1 cards carry a charge effect (+1 meter).
                If False, only the effect value-1 cards charge; basic value-1 cards have no effect.
            num_cancel_cards (int): Number of cancel cards to include in the deck. Defaults to 6.
        """
        self.card_list = []
        self.card_list.extend(self._build_cancel_cards(num_cancel_cards))
        self.card_list.extend(self._build_basic_cards(all_ones_charge))
        self.card_list.extend(self._build_effect_cards())
        self.shuffle_deck()

    def _build_cancel_cards(self, num_cancel_cards):
        return [Card(is_cancel=True) for _ in range(num_cancel_cards)]

    def _build_basic_cards(self, all_ones_charge):
        ones = [Card(1, True)] * 3 if all_ones_charge else [Card(1, False)] * 3
        return ones + [
            Card(2, False), Card(2, False), Card(2, False),
            Card(3, False), Card(3, False), Card(3, False),
            Card(4, False), Card(4, False), Card(4, False),
            Card(5, False), Card(5, False), Card(5, False),
            Card(6, False), Card(6, False), Card(6, False),
        ]

    def _build_effect_cards(self):
        return [
            Card(1, True), Card(1, True), Card(1, True),
            Card(2, True), Card(2, True), Card(2, True),
            Card(3, True), Card(3, True),
            Card(4, True), Card(4, True),
            Card(5, True), Card(5, True), Card(5, True),
            Card(6, True), Card(6, True), Card(6, True),
        ]

    def shuffle_deck(self):
        """Shuffle the card list in place."""
        random.shuffle(self.card_list)

    def draw_card(self):
        """Draw the top card from the game deck.

        Returns:
            Card: The drawn card, or None if the deck is empty.
        """
        if len(self.card_list) > 0:
            current_card = self.card_list.pop()
            return current_card
        return None

    def print_deck(self):
        """Print the total card count and each card in the deck."""
        print("TOTAL DECK CARDS:", len(self.card_list))
        for val in self.card_list:
            print(val)
