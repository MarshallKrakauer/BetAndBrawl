import random
from Card import Card

class FighterDeck:
    """Represents an individual fighter's personal deck of cards.

    Each fighter starts with a base deck of six cards (values 1-6) and can
    acquire additional cards from the game box during setup. The deck has a
    soft cap of 7 cards — adding beyond that displaces the worst card drawn.

    Attributes:
        card_list (list[Card]): Cards currently in the draw pile.
        discard (list[Card]): Cards that have already been played.
    """

    def __init__(self):
        """Initialize a FighterDeck with one card of each value (1-6)."""
        self.card_list = [Card(1), Card(2), Card(3), Card(4), Card(5), Card(6)]
        self.discard = []

    def __repr__(self):
        """Print each card in the deck to stdout."""
        for card in self.card_list:
            print(card)

    def print_deck(self):
        """Print the total card count and each card in the draw pile."""
        print("TOTAL DECK CARDS:", len(self.card_list))
        for val in self.card_list:
            print(val)

    def print_discard(self):
        """Print the total card count and each card in the discard pile."""
        print("TOTAL DISCARD CARDS:", len(self.discard))
        for val in self.discard:
            print(val)

    def shuffle_deck(self):
        """Shuffle the draw pile in place."""
        random.shuffle(self.card_list)

    def draw_card(self):
        """Draw the top card from the deck.

        Moves the drawn card to the discard pile. Returns a blank Card(0)
        if the draw pile is empty.

        Returns:
            Card: The drawn card, or Card(0) if the deck is empty.
        """
        if len(self.card_list) == 0:
            return Card(0)

        else:
            current_card = self.card_list.pop()
            self.discard.append(current_card)
            return current_card

    def add_card(self, new_card, verbose=0):
        """Add a card to the deck, shuffling it in.

        If the deck already has 7 or more cards, one card is randomly removed
        to make room for the new card.

        Args:
            new_card (Card): The card to add.
            verbose (int): If 1, prints added/removed card info. Defaults to 0.
        """
        if verbose == 1:
            print('you added...', new_card)
        if len(self.card_list) < 7:
            self.card_list.append(new_card)
            self.shuffle_deck()
        else:
            self.shuffle_deck()
            removed_card = self.card_list.pop()
            if verbose == 1:
                print('you removed...', removed_card)
            self.card_list.append(new_card)
            self.shuffle_deck()