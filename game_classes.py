import random

METER_MAX = 2
BOUT_LENGTH = 6


class Card:
    def __init__(self, value, charge=0, is_dodge=False):
        self.value = value
        self.charge = charge
        self.is_dodge = is_dodge
        if self.is_dodge:
            self.dodge_string = '\n' + 'Dodge'
        else:
            self.dodge_string = ''

    def __str__(self):
        return 'Value: ' + str(self.value) + '\n' + 'Charge:' + str(self.charge) + self.dodge_string


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


class Bout:

    def __init__(self, red_corner_deck, blue_corner_deck,  verbose=1, punch_ko_threshold=5,
                 red_corner_starting_meter = 0, blue_corner_starting_meter = 0):

        # Set up Rules of Fight
        self.round_results = ['_'] * BOUT_LENGTH
        self.punch_ko_threshold = punch_ko_threshold
        self.tko_threshold = 3

        # Set up Starting meter
        # For added clarity, "meter" refers to how much is added/subtracted
        # in current round. "charge" is how much the meter changes next round
        self.red_corner_meter = red_corner_starting_meter
        self.blue_corner_meter = blue_corner_starting_meter

        # Create decks for each fighter
        self.red_corner_deck = blue_corner_deck
        self.blue_corner_deck = red_corner_deck
        self.red_corner_deck.shuffle_deck()
        self.blue_corner_deck.shuffle_deck()

        # Initialize Fight variables to start of fight values
        self.round_number = 0
        self.previous_round_winner = 'Start of bout'
        self.round_streak = 0
        self.bout_ended_in_ko = False
        self.bout_ended_in_tko = False
        self.bout_ended_in_punch_ko = False
        self.red_corner_wins = 0
        self.blue_corner_wins = 0
        self.bout_winner = 'Draw'

        # Set verbosity: how much info will be printed out about the fight
        self.verbose = verbose


    def check_for_ko(self, winner, round_difference):
        # Draws can't possibly result in KO
        if self.previous_round_winner == 'draw':
            return False
        # Hitting a streak of three rounds is a KO
        if self.previous_round_winner == winner and self.round_streak == 2:
            self.bout_ended_in_ko = True
            self.bout_ended_in_tko = True
            return True

        # Round difference >= threshold is a punch KO
        if round_difference >= self.punch_ko_threshold:
            self.bout_ended_in_ko = True
            self.bout_ended_in_punch_ko = True
            return True

        # If neither threshold met, we have a standard non-KO round
        return False

    def handle_victory(self, winner, card_difference):
        """Handle common victory logic for both red_corner and blue_corner wins."""
        print("is it making to the handle victory function")
        # Function updates these values, if possible:
        # self.bout_ended_in_ko, self.bout_ended_in_punch_ko, self.bout_ended_in_tko
        round_resulted_in_ko = self.check_for_ko(winner, card_difference)

        # Update streak
        if winner != 'draw':
            # Fighter won multiple rounds in row ,leading to possible TKO setup
            if self.previous_round_winner == winner:
                self.round_streak += 1
            else:
                self.round_streak = 1
        else:
            # If the round was a draw, it ends the streak, no TKO is near
            self.previous_round_winner = 'draw'
            self.round_streak = 0

        # Update win counter
        if winner == 'red_corner':
            self.red_corner_wins += 1
        elif winner == 'blue_corner':
            self.blue_corner_wins += 1

        self.previous_round_winner = winner

        # Check for KO conditions
        if round_resulted_in_ko and self.verbose == 1:
            if self.bout_ended_in_punch_ko:
                print(f"{winner.upper()} PUNCH KO")
            else:
                print(f"{winner.upper()} TKO KO")

    def play_round(self):
        print(self.round_number)
        # Draw Card from each deck
        red_corner_card = self.red_corner_deck.draw_card()
        blue_corner_card = self.blue_corner_deck.draw_card()

        # Does the round involve a dodge. This creates an automated draw
        round_has_dodge = red_corner_card.is_dodge or blue_corner_card.is_dodge

        # Get values on cards. This plus meter will decide winner of round
        red_corner_card_value = red_corner_card.value
        blue_corner_card_value = blue_corner_card.value

        red_corner_charge = red_corner_card.charge
        blue_corner_charge = blue_corner_card.charge

        if self.verbose == 1:
            print("red_corner:", red_corner_card)
            print("blue_corner:", blue_corner_card)

        # Add Meter to Cards
        red_corner_round_value = red_corner_card_value + self.red_corner_meter
        blue_corner_round_value = blue_corner_card_value + self.blue_corner_meter

        # Most important_part, check for who won the round
        if round_has_dodge or red_corner_round_value == blue_corner_round_value:
            round_result = 'D'
            self.previous_round_winner = 'draw'
            self.round_streak = 0

        # Red Corner Wins the Round
        elif red_corner_round_value > blue_corner_round_value:
            round_difference = red_corner_round_value - blue_corner_round_value
            self.handle_victory('red_corner', round_difference)
            round_result = 'R'

        # Blue Corner Wins the round
        else:
            round_difference = blue_corner_round_value - red_corner_round_value
            self.handle_victory('blue_corner', round_difference)
            round_result = 'B'

        # Update Meter
        # Min/Max functions prevent value from going over 2 or under -2
        # 2 being the default, may be adjusted as game is tested

        self.blue_corner_meter = max(min(self.blue_corner_meter + blue_corner_charge,METER_MAX),METER_MAX * -1)
        self.red_corner_meter = max(min(self.red_corner_meter + red_corner_charge,METER_MAX),METER_MAX * -1)

        self.round_results[self.round_number] = round_result
        self.round_number += 1

    def fight_bout(self):
        while not self.bout_ended_in_ko and (self.round_number < len(self.round_results)):
            if self.verbose == 1:
                print("ROUND:", self.round_number + 1)
            self.play_round()

        if self.bout_ended_in_ko:
            self.bout_winner = self.previous_round_winner
            if self.verbose == 1:
                print("KO!!!!")
            # return self.previous_round_winner

        self.show_rounds()

    def show_rounds(self):
        if not self.bout_ended_in_ko:
            if self.red_corner_wins > self.blue_corner_wins:
                self.bout_winner = 'red_corner'
            elif self.red_corner_wins < self.blue_corner_wins:
                self.bout_winner = 'blue_corner'
            else:
                self.bout_winner = 'draw'
        if self.bout_ended_in_ko:
            if self.bout_ended_in_tko:
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
        if self.bout_ended_in_ko:
            decision_win = 0
        else:
            decision_win = 1
        result_dict = {'winner': self.bout_winner,
                       'ko_win': int(self.bout_ended_in_ko),
                       'tko_win': int(self.bout_ended_in_tko),
                       'punch_ko_win': int(self.bout_ended_in_punch_ko),
                       'decision_win': decision_win,
                       }
        return result_dict
