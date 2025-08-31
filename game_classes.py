import random


class Card:
    def __init__(self, value, effect=""):
        self.value = value  # Instance attribute
        self.effect = effect  # Instance attribute

    def __str__(self):
        return 'Value: ' + str(self.value) + '\n' + 'Effect:' + self.effect

    def do_thing(self):
        print(str(self.value) + '__' + str(self.effect))


class Deck:
    def __init__(self):
        self.card_list = [Card(1), Card(2), Card(3), Card(4), Card(5), Card(6)]
        self.discard = []

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
        print("DRAWING CARD")
        if len(self.card_list) == 0:
            return Card(0)  # print('oopsy doopsy')

        else:
            current_card = self.card_list.pop()
            self.discard.append(current_card)
            # print("THIS IS A CARD:", current_card)
            return current_card
            # self.print_deck()
            # self.print_discard()

    def reveal_card(self, num_reveals=1):
        value = 0
        if len(self.card_list) == 0:
            value += 0
        else:
            value += self.card_list[0].value

        if num_reveals == 2:
            if len(self.card_list) <= 1:
                value += 0
            else:
                value += self.card_list[1].value
        return value
