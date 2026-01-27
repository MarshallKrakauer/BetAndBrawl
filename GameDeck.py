from Card import Card
import random


class GameDeck:
    def __init__(self):
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

        # Placeholder for dodge cards, rule not actually in place
        dodge_cards = [Card(is_dodge=True) for _ in range(6)]
        self.card_list.extend(dodge_cards)

        # Include the main cards
        self.card_list.extend(basic_cards)
        self.card_list.extend(value_1_through_6_list)

        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.card_list)

    def draw_card(self):
        if len(self.card_list) > 0:
            current_card = self.card_list.pop()
            return current_card
        return None

    def print_deck(self):
        print("TOTAL DECK CARDS:", len(self.card_list))
        for val in self.card_list:
            print(val)
