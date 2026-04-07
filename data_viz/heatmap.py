import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Load & filter to default values ---
df = pd.read_csv(os.path.join(_DIR, "..", "all_results.csv"))

defaults = df[
    (df["bout_length"] == 6) &
    (df["meter_max"] == 2) &
    (df["fight_allows_draw"] == True) &
    (df["red_meter"] == 0) &
    (df["blue_meter"] == 0)
].copy()

# --- Compute metrics ---
draw_pct = (
    defaults[defaults["result_type"] == "draw"]
    .pivot(index="tko_threshold", columns="punch_ko_threshold", values="pct_of_outcomes")
)

ko_pct = (
    defaults[defaults["result_type"].isin(["red corner ko", "blue corner ko"])]
    .groupby(["tko_threshold", "punch_ko_threshold"])["pct_of_outcomes"]
    .sum()
    .unstack("punch_ko_threshold")
)

# --- Plot ---
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle("Fight Outcome Heatmaps\n(Bout Length: 6, Meter Max: 2, Allows Draws, Both Fighters Start with 0 Meter)", fontsize=13)

sns.heatmap(
    draw_pct,
    ax=axes[0],
    annot=True,
    fmt=".1f",
    cmap="YlGn",
    linewidths=0.5,
    cbar_kws={"label": "% of Outcomes"}
)
axes[0].set_title("% Draw")
axes[0].set_xlabel("Punch KO Threshold")
axes[0].set_ylabel("TKO Threshold")

sns.heatmap(
    ko_pct,
    ax=axes[1],
    annot=True,
    fmt=".1f",
    cmap="YlGn",
    linewidths=0.5,
    cbar_kws={"label": "% of Outcomes"}
)
axes[1].set_title("% KO (Red or Blue)")
axes[1].set_xlabel("Punch KO Threshold")
axes[1].set_ylabel("TKO Threshold")

plt.tight_layout()
plt.savefig(os.path.join(_DIR, "heatmap.png"), dpi=150, bbox_inches="tight")
plt.show()
print("Saved to heatmap.png")
