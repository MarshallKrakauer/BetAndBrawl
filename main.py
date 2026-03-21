import pandas as pd
from database import create_table, load_dataframe
from Simulator import simulate_fights


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_table()

    # List of Fights to Try
    tko_threshold = 3
    fight_li = [
        simulate_fights(num_fights=10_000, red_corner_starting_meter=0, tko_threshold=tko_threshold ),
        simulate_fights(num_fights=10_000, red_corner_starting_meter=1, tko_threshold=tko_threshold ),
        simulate_fights(num_fights=10_000, red_corner_starting_meter=1, tko_threshold=tko_threshold,
                        blue_corner_starting_meter=-1),
    ]

    result_li = []

    # Try each fight, store in result list
    for idx, fight in enumerate(fight_li):
        fight['fight_number'] = idx + 1
        result_li.append(fight)
    all_result_df = pd.concat(result_li, axis=0, ignore_index=True)
    all_result_df.to_csv('all_results.csv', index=False)
    load_dataframe(all_result_df)
