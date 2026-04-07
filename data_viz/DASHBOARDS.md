# Bet & Brawl Dashboards

Two Streamlit dashboards are available for exploring fight simulation results.

## Setup

Install dependencies:
```
py -m pip install streamlit plotly pandas
```

The dashboards read from `all_results.csv`. To regenerate it, run the simulator first:
```
py main.py
```

---

## fight_scenario_result_dashboard.py

Explores outcomes for a **single parameter combination**. Use the sidebar to filter down to one specific rule set and see a breakdown of fight results.

**Charts:** Bar chart of % of outcomes by fight result (draw, KO, decision) with corner-coded colours.

**Run:**
```
py -m streamlit run fight_scenario_result_dashboard.py
```

---

## rule_comparison_dashboard.py

Compares outcomes **across different values of a rule parameter**. Select an X axis variable to see how outcomes shift as that parameter changes, while holding the others fixed via sidebar filters.

**Charts:**
- % Draw *(hidden when draws are disabled)*
- % KO
- % Red Corner Victory *(only shown when X axis is Red Corner Meter Advantage)*

**Run:**
```
py -m streamlit run rule_comparison_dashboard.py
```
