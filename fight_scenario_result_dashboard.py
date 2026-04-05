import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Bet & Brawl Fight Simulator")

@st.cache_data
def load_data():
    df = pd.read_csv("all_results.csv")
    df["red_corner_meter_advantage"] = df["red_meter"] - df["blue_meter"]
    return df

df = load_data()

st.sidebar.header("Filters")
bout_length     = st.sidebar.selectbox("Bout Length",       sorted(df["bout_length"].unique()))
tko_threshold   = st.sidebar.selectbox("TKO Threshold",     sorted(df["tko_threshold"].unique()))
punch_ko_thresh = st.sidebar.selectbox("Punch KO Threshold",sorted(df["punch_ko_threshold"].unique()))
meter_max       = st.sidebar.selectbox("Meter Max",         sorted(df["meter_max"].unique()))
draw_label_map  = {True: "Allows Draws", False: "No Draws: Decision to Last Round Winner"}
allows_draw_label = st.sidebar.selectbox("Fight Allows Draw", ["Allows Draws", "No Draws: Decision to Last Round Winner"])
allows_draw     = {v: k for k, v in draw_label_map.items()}[allows_draw_label]
meter_advantage = st.sidebar.selectbox("Red Corner Meter Advantage", sorted(df["red_corner_meter_advantage"].unique()))

filtered = df[
    (df["bout_length"]                == bout_length)     &
    (df["tko_threshold"]              == tko_threshold)   &
    (df["punch_ko_threshold"]         == punch_ko_thresh) &
    (df["meter_max"]                  == meter_max)       &
    (df["fight_allows_draw"]          == allows_draw)     &
    (df["red_corner_meter_advantage"] == meter_advantage)
]

if filtered.empty:
    st.warning("No data for this combination.")
else:
    display = filtered[["result_type", "pct_of_outcomes"]].copy()
    display["result_type"] = display["result_type"].str.title().str.replace("Ko", "KO")
    display = display.rename(columns={"result_type": "Fight Result", "pct_of_outcomes": "% of Outcomes"})
    color_map = {
        "Red Corner KO":       "darkred",
        "Red Corner Decision": "lightcoral",
        "Blue Corner KO":      "darkblue",
        "Blue Corner Decision":"cornflowerblue",
        "Draw":                "grey",
    }
    fig = px.bar(display, x="Fight Result", y="% of Outcomes", color="Fight Result",
                 color_discrete_map=color_map)
    st.plotly_chart(fig)
    st.dataframe(display[["Fight Result", "% of Outcomes"]], hide_index=True)
