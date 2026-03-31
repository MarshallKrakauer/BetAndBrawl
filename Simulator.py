import random
import numpy as np
import pandas as pd
from Bout import Bout
from FighterDeck import FighterDeck
from GameDeck import GameDeck

_RESULT_KEYS = [
    'draw_count',
    'red_corner_ko_count',
    'red_corner_decision_count',
    'blue_corner_ko_count',
    'blue_corner_decision_count',
]


def _fresh_counters():
    """Return a zeroed-out counters dictionary."""
    return {
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
        'decision_count': 0,
    }


def process_fight_result(bout, counters, fight_number, verbose=0):
    """Process the result of a single fight and update counters.

    Args:
        bout (Bout): The completed bout object.
        counters (dict): Running totals dictionary to update in place.
        fight_number (int): The current fight index (used for verbose output).
        verbose (int): If 1, prints the result and fight number.

    Returns:
        int: fight_number incremented by 1.
    """
    result = bout.get_results()
    winner = result['winner']

    if winner == 'red_corner':
        counters['red_corner_win_count'] += 1
        counters['red_corner_ko_count' if result['ko_win'] else 'red_corner_decision_count'] += 1
    elif winner == 'blue_corner':
        counters['blue_corner_win_count'] += 1
        counters['blue_corner_ko_count' if result['ko_win'] else 'blue_corner_decision_count'] += 1
    else:
        counters['draw_count'] += 1

    counters['ko_count'] += result['ko_win']
    counters['tko_count'] += result['tko_win']
    counters['punch_ko_count'] += result['punch_ko_win']
    counters['decision_count'] += result['decision_win']

    if verbose == 1:
        print(result)
        print("End of Fight #", fight_number)

    return fight_number + 1


def simulate_fights(num_fights=10_000,
                    red_corner_starting_meter=0,
                    blue_corner_starting_meter=0,
                    random_seed=15,
                    tko_threshold=3,
                    punch_ko_threshold=5,
                    bout_length=6,
                    meter_max=2,
                    fight_allows_draw=False):
    """Simulate a batch of fights and return outcome percentages as a DataFrame.

    Args:
        num_fights (int): Number of fights to simulate. Defaults to 10,000.
        red_corner_starting_meter (int): Red corner's starting meter bonus. Defaults to 0.
        blue_corner_starting_meter (int): Blue corner's starting meter bonus. Defaults to 0.
        random_seed (int): RNG seed for reproducible results. Defaults to 15.
        tko_threshold (int): Consecutive wins needed to trigger a TKO. Defaults to 3.
        punch_ko_threshold (int): Minimum round-value gap for a punch KO. Defaults to PUNCH_KO_THRESHOLD.
        bout_length (int): Number of rounds per fight. Defaults to BOUT_LENGTH.
        meter_max (int): Maximum (and minimum as negative) meter value. Defaults to METER_MAX.
        fight_allows_draw (bool): If False, bout draws are awarded to the last
            round winner (or red_corner if all rounds tied). Defaults to False.

    Returns:
        pd.DataFrame: One row per result type with columns for outcome percentages
                      and all simulation parameters.
    """
    random.seed(random_seed)
    counters = _fresh_counters()
    fight_counter = 1

    for _ in range(num_fights):
        red_deck = FighterDeck()
        blue_deck = FighterDeck()
        game_deck = GameDeck()

        for _ in range(7):
            red_deck.add_card(game_deck.draw_card())
            blue_deck.add_card(game_deck.draw_card())

        bout = Bout(
            red_corner_deck=red_deck,
            blue_corner_deck=blue_deck,
            red_corner_starting_meter=red_corner_starting_meter,
            blue_corner_starting_meter=blue_corner_starting_meter,
            tko_threshold=tko_threshold,
            punch_ko_threshold=punch_ko_threshold,
            bout_length=bout_length,
            meter_max=meter_max,
            fight_allows_draw=fight_allows_draw,
        )
        bout.fight_bout()
        process_fight_result(bout, counters, fight_counter)
        fight_counter += 1

    rows = [
        {'result_type': key.replace('_', ' ').replace(' count', ''), 'count': counters[key]}
        for key in _RESULT_KEYS
    ]

    df = pd.DataFrame(rows)
    df['pct_of_outcomes'] = np.round(df['count'] / num_fights * 100, 1)
    df['red_meter'] = red_corner_starting_meter
    df['blue_meter'] = blue_corner_starting_meter
    df['tko_threshold'] = tko_threshold
    df['punch_ko_threshold'] = punch_ko_threshold
    df['bout_length'] = bout_length
    df['meter_max'] = meter_max
    df['fight_allows_draw'] = fight_allows_draw
    del df['count']
    return df
