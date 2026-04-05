# Bet & Brawl

A card-based fighting game simulator. Two fighters draw cards each round, and the higher value (plus accumulated meter) wins the round. Fights can end via TKO (consecutive-round streak), punch KO (large single-round value gap), or go to a decision.

## How It Works

### Core Concepts

- **Rounds** — each round both fighters draw a card. The higher total (card value + meter) wins the round.
- **Meter** — builds up over consecutive wins, adding a bonus to future rounds. Capped at a configurable max.
- **TKO** — winning a set number of consecutive rounds triggers a TKO stoppage.
- **Punch KO** — winning a round by a large enough value gap triggers an immediate KO.
- **Cancel Cards** — force a tie regardless of values, resetting momentum.
- **Reset Cards** — zero out both fighters' meters after the round.

### Configurable Rules

| Parameter | Description |
|---|---|
| Bout Length | Number of rounds (5 or 6) |
| TKO Threshold | Consecutive wins needed for a TKO (3 or 4) |
| Punch KO Threshold | Minimum value gap for a punch KO (4, 5, or 6) |
| Meter Max | Maximum meter value allowed (2 or 3) |
| Fight Allows Draw | Whether equal round wins results in a draw or decision |
| Starting Meter | Optional meter advantage for red corner |

## Running the Simulator

Install dependencies:
```
py -m pip install streamlit plotly pandas
```

Run the simulation to generate results:
```
py main.py
```

This sweeps all parameter combinations and outputs `all_results.csv`.

## Dashboards

See [DASHBOARDS.md](DASHBOARDS.md) for full dashboard documentation.

**Fight Scenario Dashboard** — explore outcomes for a single rule set:
```
py -m streamlit run fight_scenario_result_dashboard.py
```

**Rule Comparison Dashboard** — compare how outcomes shift across different values of a rule parameter:
```
py -m streamlit run rule_comparison_dashboard.py
```

## Project Structure

| File | Description |
|---|---|
| `Bout.py` | Single fight simulation logic |
| `Card.py` | Card definitions |
| `FighterDeck.py` | Fighter's draw deck |
| `GameDeck.py` | Full card pool |
| `Simulator.py` | Batch fight simulation |
| `main.py` | Parameter sweep entry point |
| `database.py` | SQLite result storage |
| `fight_scenario_result_dashboard.py` | Streamlit dashboard: compares odds of each outcome in single ruleset |
| `rule_comparison_dashboard.py` | Streamlit dashboard: compares results between different rulesets |
