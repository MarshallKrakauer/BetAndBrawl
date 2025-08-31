# This is a sample Python script.
from game_classes import Card, Deck, Bout
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    real_card = Card(5,)
    scientist_deck = Deck()
    engineer_deck = Deck()
    my_bout = Bout(home_deck=scientist_deck, away_deck=engineer_deck)
    my_bout.show_rounds()
    my_bout.play_round()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
