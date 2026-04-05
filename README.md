# Bet & Brawl

__Bet & Brawl__ is a 2-4 player betting game. While most betting games focus on races (such as __Camel Up__; __Hot Streak__; and __Ready, Set, Bet__), __Bet & Brawl__ focuses on auto-battles. Players bet on a tournament between four auto-battling robots. In each round, players may bet on the winner and means of victory (i.e. decision or KO) for the bout or exchange cards in a fighter's deck to rig the upcoming bout.

Bouts last up to 6 rounds. Each round consists of a single card draw. Two numbers decide the winner of each round: the value of the card and the meter. Each fighter's meter starts at 0, but the meter can rise or fall based on the pre-bout bets placed by the fighters or by effects written on the cards. The fighter's value for that round equals the number written on the card plus the meter. The higher value wins the round. If both values are the same (or one fighter plays a "cancel" card), the round ends in a tie. If the difference between values is at least five OR a fighter wins three consecutive rounds, the bout ends in a KO. Otherwise, the bout finishes after the 6th round. A fighter wins the bout if that fighter has won more rounds than the opponent. If both fighters win an equal number of rounds, the bout ends in a draw.

Since betting games revolve around odds, I wrote this repository to simulate bouts. The simulations allow me to set fair odds. For example, if draws occur infrequently, I can increase the payoff for correctly betting on a draw. Additionally, the simulations test various rulesets. What if a KO occurs when the difference is 4 rather than 5? What if one fighter starts the bout with a 1 meter advantage? What if we removed draws altogether, and handed the bout to the last fighter who won a round? This repository answers all those questions and more.

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
| Meter Max | Maximum meter value allowed (2 or 3). A maximum of 2 or 3 also implies a minimum of -2 or -3 |
| Fight Allows Draw | Whether equal round wins results in a draw or decision |
| Starting Meter | Red Corner Starting Meter Advantage |

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
