from itertools import product
import pandas as pd
from database import create_table, load_dataframe
from Simulator import simulate_fights


FIGHT_LENGTHS       = [5, 6]
PUNCH_KO_THRESHOLDS = [4, 5, 6]
METER_MAXES         = [2, 3]
STARTING_METERS     = [(0, 0), (1, 0), (1, -1)]   # (red, blue)
FIGHT_ALLOWS_DRAW   = [True, False]

if __name__ == '__main__':
    create_table()

    results = []
    combos = list(product(FIGHT_LENGTHS, PUNCH_KO_THRESHOLDS, METER_MAXES, STARTING_METERS, FIGHT_ALLOWS_DRAW))
    print(f"Running {len(combos)} parameter combinations...")

    for bout_length, punch_ko_thresh, meter_max, (red_meter, blue_meter), allows_draw in combos:
        df = simulate_fights(
            num_fights=10_000,
            red_corner_starting_meter=red_meter,
            blue_corner_starting_meter=blue_meter,
            punch_ko_threshold=punch_ko_thresh,
            bout_length=bout_length,
            meter_max=meter_max,
            fight_allows_draw=allows_draw,
        )
        results.append(df)

    all_result_df = pd.concat(results, axis=0, ignore_index=True)
    all_result_df.to_csv('all_results.csv', index=False)
    load_dataframe(all_result_df)
    print(f"Done. {len(all_result_df)} rows loaded.")
