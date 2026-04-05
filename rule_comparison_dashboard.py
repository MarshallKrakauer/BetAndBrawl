import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Bet & Brawl Rule Comparison")

@st.cache_data
def load_data():
    df = pd.read_csv("all_results.csv")
    df["red_corner_meter_advantage"] = df["red_meter"] - df["blue_meter"]
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

st.sidebar.header("X Axis")
x_label = st.sidebar.selectbox("X Axis Variable", list(X_AXIS_OPTIONS.keys()))
x_col   = X_AXIS_OPTIONS[x_label]

# Build filters for every variable except the X axis one
st.sidebar.header("Filters")
active_filters = {}
for label, col in X_AXIS_OPTIONS.items():
    if col == x_col:
        continue
    if col == "fight_allows_draw":
        draw_label_map = {True: "Allows Draws", False: "No Draws: Decision to Last Round Winner"}
        chosen_label = st.sidebar.selectbox(label, ["Allows Draws", "No Draws: Decision to Last Round Winner"])
        active_filters[col] = {v: k for k, v in draw_label_map.items()}[chosen_label]
    else:
        options = sorted(df[col].unique())
        active_filters[col] = st.sidebar.selectbox(label, options)

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

    st.subheader("% Draw")
    st.plotly_chart(make_chart(draw_df, "% Draw"), use_container_width=True)

    st.subheader("% KO")
    st.plotly_chart(make_chart(ko_df, "% KO"), use_container_width=True)

    st.subheader("% Red Corner Victory")
    st.plotly_chart(make_chart(red_win_df, "% Red Corner Victory"), use_container_width=True)
