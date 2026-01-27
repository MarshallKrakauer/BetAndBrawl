import random
class Card:
    def __init__(self, value=0, has_charge = False, is_dodge=False):
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
        if self.is_dodge:
            return "Dodge!"
        else:
            return 'Value: ' + str(self.value) + ';' + self.charge_string
