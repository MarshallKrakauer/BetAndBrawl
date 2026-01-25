import random
class Card:
    def __init__(self, value=0, charge=0, all_meter_reset=False, is_dodge=False):
        self.value = value
        self.charge = charge
        self.is_dodge = is_dodge
        self.all_meter_reset = all_meter_reset
        if self.all_meter_reset:
            self.charge_string = 'Reset Charge'
        else:
            self.charge_string = 'Charge:' + str(self.charge)

    def __str__(self):
        if self.is_dodge:
            return "Dodge!"
        else:
            return 'Value: ' + str(self.value) + ';' + self.charge_string
