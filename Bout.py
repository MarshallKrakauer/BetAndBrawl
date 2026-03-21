import random
from Card import Card

METER_MAX = 2
BOUT_LENGTH = 6
PUNCH_KO_THRESHOLD = 5


class Bout:
    """Simulates a single bout (fight) between two fighters.

    A bout consists of up to BOUT_LENGTH rounds. Each round both fighters draw
    a card; the higher value (plus any accumulated meter) wins the round. The
    bout ends early on a KO, which can occur via a TKO (consecutive-round
    streak) or a punch KO (large single-round value difference).

    Attributes:
        round_results (list[str]): Per-round outcome codes ('R', 'B', 'D', or '_').
        punch_ko_threshold (int): Minimum value gap required for a punch KO.
        tko_threshold (int): Consecutive wins needed to trigger a TKO.
        red_corner_meter (int): Red corner's current accumulated meter bonus.
        blue_corner_meter (int): Blue corner's current accumulated meter bonus.
        red_corner_deck (FighterDeck): Draw deck for red corner.
        blue_corner_deck (FighterDeck): Draw deck for blue corner.
        last_non_draw_winner (str): Winner of the most recent non-draw round.
        round_number (int): Index of the current round (0-based).
        previous_round_winner (str): Winner of the immediately preceding round.
        round_streak (int): Current consecutive-win streak for the leading fighter.
        bout_ended_in_ko (bool): True if the bout ended via any KO.
        bout_ended_in_tko (bool): True if the KO was a TKO (streak).
        bout_ended_in_punch_ko (bool): True if the KO was a punch KO (gap).
        red_corner_wins (int): Number of rounds won by red corner.
        blue_corner_wins (int): Number of rounds won by blue corner.
        bout_winner (str): Final winner: 'red_corner', 'blue_corner', or 'draw'.
        verbose (int): Verbosity level; 1 prints round-by-round commentary.
    """

    def __init__(self,
                 red_corner_deck,
                 blue_corner_deck,
                 verbose=0,
                 punch_ko_threshold=PUNCH_KO_THRESHOLD,
                 red_corner_starting_meter=0,
                 blue_corner_starting_meter=0,
                 tko_threshold=3):
        """Initialize a Bout between two fighters.

        Args:
            red_corner_deck (FighterDeck): The red corner fighter's card deck.
            blue_corner_deck (FighterDeck): The blue corner fighter's card deck.
            verbose (int): Verbosity level. 0 = silent, 1 = print commentary.
                Defaults to 0.
            punch_ko_threshold (int): Minimum round-value gap to trigger a punch KO.
                Defaults to PUNCH_KO_THRESHOLD.
            red_corner_starting_meter (int): Red corner's starting meter bonus.
                Defaults to 0.
            blue_corner_starting_meter (int): Blue corner's starting meter bonus.
                Defaults to 0.
            tko_threshold (int): Consecutive wins required to trigger a TKO.
                Defaults to 3.
        """

        # Set up Rules of Fight
        self.round_results = ['_'] * BOUT_LENGTH
        self.punch_ko_threshold = punch_ko_threshold
        self.tko_threshold = tko_threshold

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
        self.last_non_draw_winner = 'draw'
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
        """Determine whether the current round ends the bout via KO.

        Checks for both TKO (consecutive-win streak) and punch KO (large
        value gap). Sets the appropriate KO flags on the bout if triggered.

        Args:
            winner (str): The winner of the current round ('red_corner' or 'blue_corner').
            round_difference (int): The value gap between the two fighters this round.

        Returns:
            bool: True if a KO condition was met, False otherwise.
        """
        # Draws can't possibly result in KO
        if self.previous_round_winner == 'draw':
            return False
        # Hitting a streak of three rounds is a KO
        if self.previous_round_winner == winner and self.round_streak == self.tko_threshold - 1:
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
        if winner == 'blue_corner' or winner == 'red_corner':
            self.last_non_draw_winner = winner

        # Check for KO conditions
        if round_resulted_in_ko and self.verbose == 1:
            if self.bout_ended_in_punch_ko:
                print(f"{winner.upper()} PUNCH KO")
            else:
                print(f"{winner.upper()} TKO KO")

    def play_round(self):
        """Play a single round of the bout.

        Each fighter draws a card. The round value is the card value plus the
        fighter's current meter. The higher total wins the round. Dodge cards
        and meter-reset cards trigger special rules. Updates meters, round
        results, and the round counter.
        """
        # Draw Card from each deck
        red_corner_card = self.red_corner_deck.draw_card()
        blue_corner_card = self.blue_corner_deck.draw_card()

        # Does the round involve a Reset. This creates an automated draw
        round_has_reset = red_corner_card.all_meter_reset or blue_corner_card.all_meter_reset

        round_has_dodge = blue_corner_card.is_dodge or red_corner_card.is_dodge
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
        if round_has_dodge or (red_corner_round_value == blue_corner_round_value):
            round_result = 'D'
            self.previous_round_winner = 'draw'
            self.round_streak = 0

        # Red Corner Wins the Round
        elif red_corner_round_value > blue_corner_round_value:
            round_difference = red_corner_round_value - blue_corner_round_value
            self.handle_victory('red_corner', round_difference)
            round_result = 'R'

        # Blue Corner Wins the round
        elif blue_corner_round_value > red_corner_round_value:
            round_difference = blue_corner_round_value - red_corner_round_value
            self.handle_victory('blue_corner', round_difference)
            round_result = 'B'
        else:
            raise ValueError("No round winner was determined")

        # Update Meter
        # Min/Max functions prevent value from going over 2 or under -2
        # 2 being the default, may be adjusted as game is tested

        if round_has_dodge:
            pass # Dodge Cancels all effect
        elif round_has_reset:
            self.red_corner_meter, self.blue_corner_meter = 0, 0
        else:
            self.blue_corner_meter = max(min(self.blue_corner_meter + blue_corner_charge, METER_MAX), METER_MAX * -1)
            self.red_corner_meter = max(min(self.red_corner_meter + red_corner_charge, METER_MAX), METER_MAX * -1)

        self.round_results[self.round_number] = round_result
        self.round_number += 1

    def fight_bout(self):
        """Run all rounds of the bout until completion.

        Plays rounds until a KO occurs or the maximum number of rounds is
        reached, then calls show_rounds() to finalize the result.
        """
        while not self.bout_ended_in_ko and (self.round_number < len(self.round_results)):
            if self.verbose == 1:
                print("ROUND:", self.round_number + 1)
            self.play_round()

        if self.bout_ended_in_ko:
            self.bout_winner = self.previous_round_winner
            if self.verbose == 1:
                print("KO!!!!")
        # if self.bout_winner == 'Draw':
        #     self.bout_winner = self.previous_round_winner
        #print(self.bout_winner)
        self.show_rounds()

    def show_rounds(self):
        """Finalize and optionally display the bout result.

        Determines the bout winner by round count (if no KO) and the win
        method (Decision, KO (TKO), or KO (Punch)). Prints a summary when
        verbose is enabled.
        """
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
        """Return a summary dictionary of the bout outcome.

        Returns:
            dict: A dictionary with the following keys:
                - 'winner' (str): 'red_corner', 'blue_corner', or 'draw'.
                - 'ko_win' (int): 1 if the bout ended in any KO, else 0.
                - 'tko_win' (int): 1 if the bout ended in a TKO, else 0.
                - 'punch_ko_win' (int): 1 if the bout ended in a punch KO, else 0.
                - 'decision_win' (int): 1 if the bout went to decision, else 0.
        """
        #if self.bout_winner == 'draw':
        #    self.bout_winner = self.last_non_draw_winner
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
