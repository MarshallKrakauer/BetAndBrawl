import random


class Card:
    """Represents a single card in the BetAndBrawl card game.

    Each card has a numeric value used to determine round winners, and may
    carry a charge effect that modifies a fighter's meter in subsequent rounds.
    Cards can also be dodge cards, which force a draw for that round.

    Attributes:
        value (int): The numeric value of the card (0-6).
        is_dodge (bool): Whether this card is a dodge card.
        charge (int): Meter change applied next round (+1, -1, or 0).
        all_meter_reset (bool): Whether this card resets both fighters' meters to zero.
        charge_string (str): Human-readable description of the charge effect.
    """

    def __init__(self, value=0, has_charge=False, is_dodge=False):
        """Initialize a Card.

        Args:
            value (int): The numeric value of the card. Defaults to 0.
            has_charge (bool): Whether this card carries a charge effect.
                Cards with values 1-2 gain +1 charge, values 5-6 gain -1 charge,
                and values 3-4 trigger an all-meter reset. Defaults to False.
            is_dodge (bool): Whether this card is a dodge card, which forces
                a draw for the round. Defaults to False.
        """
        # Set default values of cards
        self.charge = 0
        self.all_meter_reset = False
        self.value = value
        self.is_dodge = is_dodge

        # For cards that charge/drain, change their values
        if has_charge:
            if self.value in (1,2):
                self.charge = 1
            elif self.value in (5,6):
                self.charge = -1
            elif self.value in (3,4):
                self.all_meter_reset = True

        # Get string value of charge
        if self.all_meter_reset:
            self.charge_string = 'Reset Charge'
        else:
            self.charge_string = 'Charge:' + str(self.charge)

    def __str__(self):
        """Return a human-readable string representation of the card.

        Returns:
            str: 'Dodge!' for dodge cards, otherwise the card value and charge info.
        """
        if self.is_dodge:
            return "Dodge!"
        else:
            return 'Value: ' + str(self.value) + ';' + self.charge_string
