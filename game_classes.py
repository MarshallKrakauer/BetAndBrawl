import random

METER_MAX = 2
BOUT_LENGTH = 6


class Card:
    def __init__(self, value, charge=0, is_dodge=False):
        self.value = value
        self.charge = charge
        self.is_dodge = is_dodge

    def __str__(self):
        'Value: ' + str(self.value) + '\n' + 'Charge:' + self.effect


class GameDeck:
    def __init__(self):
        self.card_list = []
        basic_cards = [Card(1), Card(1), Card(1), Card(1),
                       Card(2)]

        self.card_list.extend()


class FighterDeck:
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
            return Card(0)

        else:
            current_card = self.card_list.pop()
            self.discard.append(current_card)
            return current_card


class Bout:

    def __init__(self, red_corner_deck, blue_corner_deck,  verbose=0):
        self.round_results = ['_'] * BOUT_LENGTH
        self.red_corner_deck = blue_corner_deck
        self.blue_corner_deck = red_corner_deck
        self.red_corner_deck.shuffle_deck()
        self.blue_corner_deck.shuffle_deck()
        self.round_number = 0
        self.previous_round_winner = 'Start of bout'
        self.round_streak = 0
        self.punch_ko_threshold = 5
        self.has_ko = False
        self.has_tko = False
        self.has_punch_ko = False
        self.red_corner_wins = 0
        self.blue_corner_wins = 0
        self.bout_winner = 'Draw'
        self.verbose = verbose
        self.tko_threshold = 3

    def check_for_ko(self, winner, card_difference):
        if self.previous_round_winner == winner and self.round_streak == 2:
            return True
        if card_difference >= self.punch_ko_threshold:
            return True
        return False

    def handle_victory(self, winner, card_difference):
        """Handle common victory logic for both red_corner and blue_corner wins."""

        if winner == 'draw':
            is_ko = False
        else:
            is_ko = self.check_for_ko(winner, card_difference)

        if is_ko and winner == 'blue_corner':
            winner = 'blue_corner'
        if is_ko and winner == 'red_corner':
            winner = 'red_corner'

        # Update streak
        if winner != 'draw':
            if self.previous_round_winner == winner:
                self.round_streak += 1
            else:
                self.round_streak = 1
        else:
            self.previous_round_winner = 'draw'
            self.round_streak = 0

        self.previous_round_winner = winner

        # Update win counter
        if winner == 'red_corner':
            self.red_corner_wins += 1
        elif winner == 'blue_corner':
            self.blue_corner_wins += 1

        # Check for KO conditions
        if card_difference >= self.punch_ko_threshold:
            if self.verbose == 1:
                print(f"{winner.upper()} PUNCH KO")
            self.has_ko, self.has_punch_ko = True, True

        if self.round_streak == self.tko_threshold:
            if self.verbose == 1:
                print(f"{winner.upper()} TKO")
            self.has_ko, self.has_tko = True, True

    def play_round(self):
        red_corner_card = self.red_corner_deck.draw_card()
        blue_corner_card = self.blue_corner_deck.draw_card()
        red_corner_value = red_corner_card.value
        blue_corner_value = blue_corner_card.value
        if self.verbose == 2:
            print("red_corner:", red_corner_card)
            print("blue_corner:", blue_corner_card)
        card_difference = 0
        round_result = ''

        # Main logic becomes:
        if red_corner_card.value > blue_corner_card.value:
            card_difference = red_corner_value - blue_corner_value
            self.handle_victory('red_corner', card_difference)
            round_result = 'H'
        elif blue_corner_card.value > red_corner_card.value:
            card_difference = blue_corner_value - red_corner_value
            self.handle_victory('blue_corner', card_difference)
            round_result = 'A'
        else:
            round_result = 'D'
            self.previous_round_winner = 'draw'
            self.round_streak = 0

        self.round_results[self.round_number] = round_result
        self.round_number += 1

    def fight_bout(self):
        while not self.has_ko and (self.round_number < len(self.round_results)):
            if self.verbose == 1:
                print("ROUND:", self.round_number + 1)
            self.play_round()

        if self.has_ko:
            self.bout_winner = self.previous_round_winner
            if self.verbose == 1:
                print("KO!!!!")
            # return self.previous_round_winner

        self.show_rounds()

    def show_rounds(self):
        if not self.has_ko:
            if self.red_corner_wins > self.blue_corner_wins:
                self.bout_winner = 'red_corner'
            elif self.red_corner_wins < self.blue_corner_wins:
                self.bout_winner = 'blue_corner'
            else:
                self.bout_winner = 'draw'
        if self.has_ko:
            if self.has_tko:
                win_method = 'KO (TKO)'
            else:
                win_method = 'KO (Punch)'
        else:
            win_method = 'Decision'

        if self.verbose == 1:
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
