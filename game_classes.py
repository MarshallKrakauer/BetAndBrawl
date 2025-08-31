import random


class Card:
    def __init__(self, value, effect=""):
        self.value = value  # Instance attribute
        self.effect = effect  # Instance attribute

    def __str__(self):
        if self.effect != "":
            return 'Value: ' + str(self.value) + '\n' + 'Effect:' + self.effect
        else:
            return 'Value: ' + str(self.value)

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
            # print("THIS IS A CARD:", current_card)
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
        self.round_results = ['_'] * bout_length
        self.home_deck = home_deck
        self.away_deck = away_deck
        self.home_deck.shuffle_deck()
        self.away_deck.shuffle_deck()
        self.round_number = 0
        self.previous_round_winner = 'Start of bout'
        self.round_streak = 0
        self.ko_threshold = 5
        self.has_ko = False
        self.has_tko = False
        self.has_punch_ko = False
        self.home_wins = 0
        self.away_wins = 0
        self.bout_winner = 'Draw'
        self.verbose = False
        self.tko_threshold = 3

    def play_round(self):
        home_card = self.home_deck.draw_card()
        away_card = self.away_deck.draw_card()
        home_value = home_card.value
        away_value = away_card.value
        if self.verbose:
            print("HOME:", home_card)
            print("AWAY:", away_card)
        card_difference = 0
        round_result = ''

        # HOME VICTORY
        if home_card.value > away_card.value:
            card_difference = home_value - away_value
            #print('HOME WINS')
            if self.previous_round_winner == 'home':
                self.round_streak += 1
            else:
                self.round_streak = 1
            self.previous_round_winner = 'home'
            round_result = 'H'
            self.home_wins += 1
            if card_difference >= self.ko_threshold:
                print("HOME PUNCH KO")
                self.has_ko, self.has_punch_ko = True, True
            if self.round_streak == self.tko_threshold:
                print("HOME TKO")
                self.has_ko, self.has_tko = True, True

        ## Away Victory
        elif away_card.value > home_card.value:
            card_difference = away_value - home_value
            #print('AWAY WINS')
            if self.previous_round_winner == 'away':
                self.round_streak += 1
            else:
                self.round_streak = 1
            self.previous_round_winner = 'away'
            round_result = 'A'
            self.away_wins += 1
            if card_difference >= self.ko_threshold:
                print("AWAY PUNCH KO")
                self.has_ko, self.has_punch_ko = True, True
            if self.round_streak == self.tko_threshold:
                print("AWAY TKO")
                self.has_ko, self.has_tko = True, True
        else:
            #print('DRAW')
            round_result = 'D'
            self.previous_round_winner = 'draw'
            self.round_streak = 0

        self.round_results[self.round_number] = round_result
        self.round_number += 1
        #print("### ROUND STREAK ### ", self.round_streak)

    def fight_bout(self):
        while not self.has_ko and (self.round_number < len(self.round_results)):
            print("ROUND:", self.round_number + 1)
            self.play_round()

        if self.has_ko:
            self.bout_winner = self.previous_round_winner
            print("KO!!!!")
            # return self.previous_round_winner

        self.show_rounds()

    def show_rounds(self):
        if not self.has_ko:
            if self.home_wins > self.away_wins:
                self.bout_winner = 'home'
            elif self.home_wins < self.away_wins:
                self.bout_winner = 'away'
            else:
                self.bout_winner = 'draw'
        if self.has_ko:
            win_method = 'KO'
        else:
            win_method = 'Decision'

        print(len(self.round_results))
        print(self.round_results)
        print("THE FINAL RESULT", self.bout_winner, 'by', win_method)

    def get_results(self):
        if self.has_ko:
            decision_win = 0
        else:
            decision_win = 1
        result_dict = {'winner': self.bout_winner,
                       'ko_win': int(self.has_ko),
                       'tko_win': int(self.has_tko),
                       'punch_ko_win': int(self.has_punch_ko),
                       'decision_win': decision_win,
                       }
        return result_dict
