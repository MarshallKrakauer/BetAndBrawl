# This is a sample Python script.
import random
from game_classes import Card, Deck, Bout

counters = {
    'home_win_count': 0,
    'away_win_count': 0,
    'draw_count': 0,
    'home_ko_count': 0,
    'home_decision_count': 0,
    'away_ko_count': 0,
    'away_decision_count': 0,
    'ko_count': 0,
    'tko_count': 0,
    'punch_ko_count': 0,
    'decision_count': 0
}


def process_fight_result(bout, counters, fight_number):
    """
    Process the result of a fight and update all relevant counters.

    Args:
        bout: The bout object to get results from
        counters: Dictionary containing all counter variables
        fight_number: Current fight number

    Returns:
        Updated fight_number (incremented by 1)
    """
    result_of_fight = bout.get_results()
    winner = result_of_fight['winner']
    ko_win = result_of_fight['ko_win']

    # Update win counters
    if winner == 'home':
        counters['home_win_count'] += 1
        if ko_win == 1:
            counters['home_ko_count'] += 1
        else:
            counters['home_decision_count'] += 1
    elif winner == 'away':
        counters['away_win_count'] += 1
        if ko_win == 1:
            counters['away_ko_count'] += 1
        else:
            counters['away_decision_count'] += 1
    else:
        counters['draw_count'] += 1

    # Update other fight outcome counters
    counters['ko_count'] += result_of_fight['ko_win']
    counters['tko_count'] += result_of_fight['tko_win']
    counters['punch_ko_count'] += result_of_fight['punch_ko_win']
    counters['decision_count'] += result_of_fight['decision_win']

    print(result_of_fight)
    print("End of Fight #", str(fight_number))

    return fight_number + 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 10 is Away TKO
    # 11, 12, 13 are draw
    home_win_count, away_win_count, draw_count = 0, 0, 0
    home_ko_count, home_decision_count, away_ko_count, away_decision_count = 0, 0, 0, 0
    ko_count, tko_count, punch_ko_count, decision_count = 0, 0, 0, 0
    random.seed(15)
    num_fights = 10_000
    fight_counter = 1
    while fight_counter <= num_fights:
        scientist_deck = Deck()
        engineer_deck = Deck()
        my_bout = Bout(home_deck=scientist_deck, away_deck=engineer_deck
                       , home_support_count=0
                       , away_support_count=0)
        my_bout.fight_bout()
        result_of_fight = my_bout.get_results()
        process_fight_result(my_bout, counters, fight_counter)
        fight_counter += 1

    if True:
        print("#### WIN METHODS ####")
        print('Decision Count', decision_count)
        print('KO count', ko_count)
        print('TKO Count', tko_count)
        print('Punch KO Count', punch_ko_count)

        print("### BET TYPES ###")
        print('Home KO:', home_ko_count)
        print('Home Decision:', home_decision_count)
        print('Draw:', draw_count)
        print('Away Decision:', away_decision_count)
        print('Away KO:', away_ko_count)

    """
    Home KO: 227
    Home Decision: 152
    Draw: 250
    Away Decision: 132
    Away KO: 239
    """
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
