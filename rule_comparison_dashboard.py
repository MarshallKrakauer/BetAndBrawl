import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Bet & Brawl Rule Comparison")

@st.cache_data
def load_data():
    df = pd.read_csv("all_results.csv")
    df["red_corner_meter_advantage"] = df["red_meter"] - df["blue_meter"]
    df["fight_allows_draw"] = df["fight_allows_draw"].map(
        {True: "Allows Draws", False: "No Draws: Decision to Last Round Winner"}
    )
    return df

df = load_data()

X_AXIS_OPTIONS = {
    "Bout Length":                "bout_length",
    "TKO Threshold":              "tko_threshold",
    "Punch KO Threshold":         "punch_ko_threshold",
    "Meter Max":                  "meter_max",
    "Fight Allows Draw":          "fight_allows_draw",
    "Red Corner Meter Advantage": "red_corner_meter_advantage",
}

DEFAULTS = {
    "bout_length":                6,
    "tko_threshold":              3,
    "punch_ko_threshold":         5,
    "meter_max":                  2,
    "fight_allows_draw":          "Allows Draws",
    "red_corner_meter_advantage": 0,
}

st.sidebar.header("X Axis")
x_label = st.sidebar.selectbox("X Axis Variable", list(X_AXIS_OPTIONS.keys()))
x_col   = X_AXIS_OPTIONS[x_label]

st.sidebar.header("Filters")
active_filters = {}
for label, col in X_AXIS_OPTIONS.items():
    if col == x_col:
        continue
    options = sorted(df[col].unique())
    default_val = DEFAULTS[col]
    default_idx = options.index(default_val) if default_val in options else 0
    if col == "fight_allows_draw":
        tooltip = "By default, the bout draws when both fighters win the same number of rounds. Instead, we can choose a ruleset where, if the fighters win the same number of rounds, the most recent fighter to win receives a decision victory. In the rare case that all rounds tie, the red corner wins by decision."
    elif col == "red_corner_meter_advantage":
        tooltip = "0 means both fighters start with 0 meter; 1 means Red starts with 1 and Blue with 0; 2 means Red starts with 1 and Blue with -1"
    else:
        tooltip = None
    active_filters[col] = st.sidebar.selectbox(
        f"{label} (Default: {default_val})", options, index=default_idx, help=tooltip
    )

# Apply filters
filtered = df.copy()
for col, val in active_filters.items():
    filtered = filtered[filtered[col] == val]

if filtered.empty:
    st.warning("No data for this combination.")
else:
    grouped = filtered.groupby([x_col, "result_type"], as_index=False)["pct_of_outcomes"].mean()
    pivot   = grouped.pivot_table(index=x_col, columns="result_type", values="pct_of_outcomes").reset_index()
    x_tickvals = sorted(pivot[x_col].unique())

    draw_df = pivot[[x_col, "draw"]].rename(columns={x_col: x_label, "draw": "% Draw"})

    ko_df = pivot[[x_col]].copy()
    ko_df["% KO"] = pivot["red corner ko"] + pivot["blue corner ko"]
    ko_df = ko_df.rename(columns={x_col: x_label})

    red_win_df = pivot[[x_col]].copy()
    red_win_df["% Red Corner Victory"] = pivot["red corner ko"] + pivot["red corner decision"]
    red_win_df = red_win_df.rename(columns={x_col: x_label})

    def make_chart(df, y_col):
        fig = px.bar(df, x=x_label, y=y_col)
        fig.update_xaxes(tickmode="array", tickvals=x_tickvals)
        return fig

    if active_filters.get("fight_allows_draw") != "No Draws: Decision to Last Round Winner":
        st.subheader("% Draw")
        st.plotly_chart(make_chart(draw_df, "% Draw"), use_container_width=True)

    st.subheader("% KO")
    st.plotly_chart(make_chart(ko_df, "% KO"), use_container_width=True)

    if x_col == "red_corner_meter_advantage":
        st.subheader("% Red Corner Victory")
        st.plotly_chart(make_chart(red_win_df, "% Red Corner Victory"), use_container_width=True)
