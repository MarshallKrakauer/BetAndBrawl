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

    def __init__(self):
        """Initialize a GameDeck with all basic, charge-effect, and cancel cards, then shuffle."""
        self.card_list = []

        # Initialize the basic cards with no effect
        basic_cards = [
            Card(1, False), Card(1, False), Card(1, False),
            Card(2, False), Card(2, False), Card(2, False),
            Card(3, False), Card(3, False), Card(3, False),
            Card(4, False), Card(4, False), Card(4, False),
            Card(5, False), Card(5, False), Card(5, False),
            Card(6, False), Card(6, False), Card(6, False),
        ]

        value_1_through_6_list = [
            # Dupe 1 and 2
            Card(1, True),
            Card(1, True),
            Card(1, True),

            Card(2, True),
            Card(2, True),
            Card(2, True),

            Card(3, True),
            Card(3, True),

            Card(4, True),
            Card(4, True),

            # Dupe 5 and 6
            Card(5, True),
            Card(5, True),
            Card(5, True),

            Card(6, True),
            Card(6, True),
            Card(6, True)
        ]

        # Cancel cards force a draw for the round
        cancel_cards = [Card(is_cancel=True) for _ in range(6)]
        self.card_list.extend(cancel_cards)

        # Include the main cards
        self.card_list.extend(basic_cards)
        self.card_list.extend(value_1_through_6_list)

        self.shuffle_deck()

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
