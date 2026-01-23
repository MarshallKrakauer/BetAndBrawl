# This is a sample Python script.
import random
from game_classes import Card, FighterDeck, Bout, GameDeck


def process_fight_result(bout, counters, fight_number, verbose=0):
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
    if winner == 'red_corner':
        counters['red_corner_win_count'] += 1
        if ko_win == 1:
            counters['red_corner_ko_count'] += 1
        else:
            counters['red_corner_decision_count'] += 1
    elif winner == 'blue_corner':
        counters['blue_corner_win_count'] += 1
        if ko_win == 1:
            counters['blue_corner_ko_count'] += 1
        else:
            counters['blue_corner_decision_count'] += 1
    else:
        counters['draw_count'] += 1

    # Update other fight outcome counters
    counters['ko_count'] += result_of_fight['ko_win']
    counters['tko_count'] += result_of_fight['tko_win']
    counters['punch_ko_count'] += result_of_fight['punch_ko_win']
    counters['decision_count'] += result_of_fight['decision_win']

    if verbose == 1:
        print(result_of_fight)
        print("End of Fight #", str(fight_number))

    return fight_number + 1


def simulate_fights(num_fights=10_000, red_corner_starting_meter=0,
                    blue_corner_starting_meter=0, ):
    num_fights = num_fights
    fight_counter = 1
    counters = {
        'red_corner_win_count': 0,
        'blue_corner_win_count': 0,
        'draw_count': 0,
        'red_corner_ko_count': 0,
        'red_corner_decision_count': 0,
        'blue_corner_ko_count': 0,
        'blue_corner_decision_count': 0,
        'ko_count': 0,
        'tko_count': 0,
        'punch_ko_count': 0,
        'decision_count': 0
    }
    while fight_counter <= num_fights:
        # Set up the two rival fighters
        marshall_deck = FighterDeck()
        andre_deck = FighterDeck()

        # Set up the deck to draw from and the fighters
        cards_in_game_box = GameDeck()
        my_bout = Bout(blue_corner_deck=marshall_deck, red_corner_deck=andre_deck, verbose=0,
                       blue_corner_starting_meter=blue_corner_starting_meter,
                       red_corner_starting_meter=red_corner_starting_meter)

        for i in range(7):
            marshall_deck.add_card(cards_in_game_box.draw_card())
            andre_deck.add_card(cards_in_game_box.draw_card())

        my_bout.fight_bout()
        result_of_fight = my_bout.get_results()
        process_fight_result(my_bout, counters, fight_counter, 0)
        fight_counter += 1

    for key, value in counters.items():
        if key in ['draw_count', 'red_corner_ko_count', 'red_corner_decision_count',
                   'blue_corner_ko_count', 'blue_corner_decision_count']:
            print(key.replace('_', ' '), value)
    print('\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    random.seed(15)

    # marshall_deck = FighterDeck()
    # andre_deck = FighterDeck()
    # ian_deck = FighterDeck()
    # cards_in_game_box = GameDeck()
    #
    # for i in range(10):
    #     print('######Iteration:', str(i + 1), '######')
    #     my_card = cards_in_game_box.draw_card()
    #     marshall_deck.add_card(my_card)
    #     marshall_deck.print_deck()

    # No Meter
    simulate_fights(num_fights=10_000, red_corner_starting_meter=0, blue_corner_starting_meter=0)

    # 1 Red Meter
    simulate_fights(num_fights=10_000, red_corner_starting_meter=1, blue_corner_starting_meter=0)

    # 2 Red Meter
    simulate_fights(num_fights=10_000, red_corner_starting_meter=2, blue_corner_starting_meter=0)

    # 1 Meter Each
    simulate_fights(num_fights=10_000, red_corner_starting_meter=1, blue_corner_starting_meter=1)
