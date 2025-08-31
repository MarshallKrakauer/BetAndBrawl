# This is a sample Python script.
import random
from game_classes import Card, Deck, Bout


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 10 is Away TKO
    # 11, 12, 13 are draw
    home_win_count, away_win_count, draw_count, ko_count = 0, 0, 0, 0
    tko_count, punch_ko_count, decision_count = 0, 0, 0
    random.seed(15)
    real_card = Card(5, )
    scientist_deck = Deck()
    engineer_deck = Deck()
    my_bout = Bout(home_deck=scientist_deck, away_deck=engineer_deck)
    # my_bout.show_rounds()
    my_bout.fight_bout()
    result_of_fight = my_bout.get_results()
    if result_of_fight['winner'] == 'home':
        home_win_count += 1
    elif result_of_fight['winner'] == 'away':
        away_win_count += 1
    else:
        draw_count += 1
    ko_count += result_of_fight['ko_win']
    tko_count += result_of_fight['tko_win']
    punch_ko_count += result_of_fight['punch_ko_win']
    decision_count
    print(result_of_fight)
    print(ko_count, tko_count, punch_ko_count)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
