import random
from Card import Card

class FighterDeck:
    def __init__(self):
        self.card_list = [Card(1), Card(2), Card(3), Card(4), Card(5), Card(6)]
        self.discard = []

    def __repr__(self):
        for card in self.card_list:
            print(card)

    def print_deck(self):
        print("TOTAL DECK CARDS:", len(self.card_list))
        for val in self.card_list:
            print(val)

    def print_discard(self):
        print("TOTAL DISCARD CARDS:", len(self.discard))
        for val in self.discard:
            print(val)

    def shuffle_deck(self):
        random.shuffle(self.card_list)

    def draw_card(self):
        if len(self.card_list) == 0:
            return Card(0)

        else:
            current_card = self.card_list.pop()
            self.discard.append(current_card)
            return current_card

    def add_card(self, new_card, verbose=0):
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