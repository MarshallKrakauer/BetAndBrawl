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
        if len(self.card_list) == 0:
            return Card(0)  # print('oopsy doopsy')

        else:
            current_card = self.card_list.pop()
            self.discard.append(current_card)
            print("THIS IS A CARD:", current_card)
            return current_card
            # self.print_deck()
            # self.print_discard()

    def reveal_card(self, num_reveals=1):
        if num_reveals > 2:
            num_reveals = 2
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
        print("VALUE REVEALED:", value)
        return value


class Bout:

    def __init__(self, home_deck, away_deck, bout_length=6):
        self.rounds = ['_'] * bout_length
        self.home_deck = home_deck
        self.away_deck = away_deck
        self.home_deck.shuffle_deck()
        self.away_deck.shuffle_deck()
        self.round_number = 0

    def play_round(self):
        home_card = self.home_deck.draw_card()
        away_card = self.away_deck.draw_card()
        print("HOME:", home_card)
        print("AWAY:", away_card)
        if home_card.value > away_card.value:
            print('HOME WINS')
        elif away_card.value > home_card.value:
            print('AWAY WINS')
        else:
            print('DRAW')

    def show_rounds(self):
        print(len(self.rounds))
        print(self.rounds)
