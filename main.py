# This is a sample Python script.
import random
import numpy as np
import pandas as pd
import copy
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
                    blue_corner_starting_meter=0, super_charge_value=2,random_seed=15):
    """
    Simulate fights in order to get odds

    Args:
        num_fights: How many fights to simulate. 10K seems to be enough
        red_corner_starting_meter = how much meter (bonus fight value) the red corner starts with
        blue_corner_starting_meter = how meter (bonus fight value) the blue corner starts with
        super_charge_value: Used to check if odds are different when 1,2,6,7 add or subtract 2 charge
        random_seed: Set starting point for RNG, used ot get predictable outcomes

    Returns:
        pandas dataframe with key data from fights
    """
    random.seed(15)
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
        cards_in_game_box = GameDeck(max_charge_value_abs_value=super_charge_value)
        my_bout = Bout(blue_corner_deck=marshall_deck, red_corner_deck=andre_deck, verbose=0,
                       blue_corner_starting_meter=blue_corner_starting_meter,
                       red_corner_starting_meter=red_corner_starting_meter)

        for i in range(7):
            marshall_deck.add_card(cards_in_game_box.draw_card())
            andre_deck.add_card(cards_in_game_box.draw_card())

        my_bout.fight_bout()
        # result_of_fight = my_bout.get_results()
        process_fight_result(my_bout, counters, fight_counter, 0)
        fight_counter += 1

    rows = []

    for key, value in counters.items():
        if key in [
            'draw_count',
            'red_corner_ko_count',
            'red_corner_decision_count',
            'blue_corner_ko_count',
            'blue_corner_decision_count'
        ]:
            rows.append({
                'result_type': key.replace('_', ' ').replace(' count', ''),
                'count': value
            })

    df = pd.DataFrame(rows)
    df['red_meter'] = red_corner_starting_meter
    df['blue_meter'] = blue_corner_starting_meter
    df['pct_of_outcomes'] = np.round(df['count'] / num_fights * 100, 1)
    del df['count']  # Remove count once we get the percentages
    df['super_charge_Value'] = super_charge_value
    return df


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # List of Fights to Try
    fight_li = [simulate_fights(num_fights=10_000, red_corner_starting_meter=0),
                simulate_fights(num_fights=10_000, red_corner_starting_meter=0, super_charge_value=1),
                simulate_fights(num_fights=10_000, red_corner_starting_meter=1),
                simulate_fights(num_fights=10_000, red_corner_starting_meter=1, super_charge_value=1),
                simulate_fights(num_fights=10_000, red_corner_starting_meter=2),
                simulate_fights(num_fights=10_000, red_corner_starting_meter=2, super_charge_value=1),
                ]

    result_li = []

    # Try each fight, store in result list
    for idx, fight in enumerate(fight_li):
        fight['fight_number'] = idx + 1
        result_li.append(fight)
    all_result_df = pd.concat(result_li, axis=0, ignore_index=True)
    all_result_df.to_csv('all_results.csv', index=False)
