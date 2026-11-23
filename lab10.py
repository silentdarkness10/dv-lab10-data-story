"""TFB3133/TEB3133 Data Visualization - Lab 10: Framing the Data Story.

Run locally:  streamlit run lab10.py

All ratings are FICTIONAL practice averages (1-5 scale), not findings from a real survey.
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Lab 10 | Data Story", layout="wide")

# ---------------------------------------------------------------- data ----
SKILLS = ["Data storytelling", "Python", "Chart selection",
          "Color and labels", "Data cleaning"]

# Original lab values (Python = 3.0).
ORIGINAL = [2.4, 3.0, 3.2, 3.7, 4.1]
# Assignment Part 2: ONE rating changed -> Python 3.0 becomes 2.1,
# so Python (not data storytelling) is now the lowest average.
MODIFIED = [2.4, 2.1, 3.2, 3.7, 4.1]

ORANGE, BLUE = "#E07A3F", "#4C78A8"

# ------------------------------------------------------------- sidebar ----
with st.sidebar:
    st.header("Story settings")
    audience = st.radio(
        "Who is this story for?",
        ["Students planning a workshop",
         "Workshop instructor",
         "Department manager"],
    )
    scenario = st.radio(
        "Which ratings?",
        ["Modified (Python changed to 2.1)", "Original lab values"],
        help="Switch to see how changing ONE rating changes the takeaway.",
    )
    st.caption("The title, highlighted bar and text all update from the data, "
               "so they always agree with each other.")

ratings = MODIFIED if scenario.startswith("Modified") else ORIGINAL

# Sort ascending so the lowest skill sits at the top (position is a cue too).
df = (pd.DataFrame({"Skill": SKILLS, "Average rating": ratings})
      .sort_values("Average rating").reset_index(drop=True))

weakest = df.loc[0, "Skill"]
# Keep proper nouns (e.g. "Python") capitalised inside a sentence.
weakest_txt = weakest if weakest == "Python" else weakest.lower()
low = df.loc[0, "Average rating"]
gap = df.loc[1, "Average rating"] - low  # distance to the next-lowest skill

# --------------------------------------------------------- audience copy ----
# Same data, three different questions -> three different titles/takeaways.
FRAMES = {
    "Students planning a workshop": {
        "title": "Plan a Workshop Around Students' Needs",
        "audience": "Students who self-rated their data visualization skills "
                    "and are planning a workshop.",
        "question": "Which skill should the next workshop cover?",
        "takeaway": f"Make {weakest_txt} the focus of the next workshop.",
        "why": f"{weakest} has the lowest average self-rating ({low:.1f} out of 5).",
    },
    "Workshop instructor": {
        "title": f"Teach {weakest} First",
        "audience": "The instructor who will design and deliver the workshop.",
        "question": "Which topic should I spend most of my session time on?",
        "takeaway": f"Open the session with {weakest_txt}; "
                    f"the group is least confident here.",
        "why": f"At {low:.1f} out of 5 it is {gap:.1f} points below the "
               f"next-lowest skill, so it needs the most teaching time.",
    },
    "Department manager": {
        "title": f"Training Priority: {weakest}",
        "audience": "A department manager deciding how to use limited "
                    "training time and budget.",
        "question": "Which single skill gap is worth supporting first?",
        "takeaway": f"Approve one workshop on {weakest_txt}; "
                    f"other skills are already stronger.",
        "why": f"{weakest} is the weakest skill ({low:.1f} out of 5), "
               f"while the strongest ({df['Average rating'].max():.1f}) "
               f"needs little support.",
    },
}
frame = FRAMES[audience]

# --------------------------------------------------------------- header ----
st.title(frame["title"])
st.write(f"**Audience:** {frame['audience']}")
st.write(f"**Their question:** {frame['question']}")
st.success(f"**Takeaway:** {frame['takeaway']}")

# ---------------------------------------------------------------- chart ----
fig, ax = plt.subplots(figsize=(8, 4.5))
colors = [ORANGE] + [BLUE] * (len(df) - 1)  # one contrasting colour = one point
bars = ax.barh(df["Skill"], df["Average rating"], color=colors)

ax.set_xlim(0, 5)                      # zero baseline, full 1-5 scale visible
ax.set_xticks(range(0, 6))
# Changed after feedback: a reader was unsure why the axis starts at 0 when
# the scale is 1-5, so the label now says bars are drawn from 0.
ax.set_xlabel("Average self-rating (1 = beginner, 5 = confident; bars drawn from 0)")
ax.set_title(f"{weakest} received the lowest average rating", loc="left")
ax.invert_yaxis()
# Removed: the vertical grid lines. Bars are labelled directly, so the grid
# only added clutter that competed with the highlighted bar.
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for i, (bar, value) in enumerate(zip(bars, df["Average rating"])):
    y = bar.get_y() + bar.get_height() / 2
    if i == 0:
        # Text annotation: extra emphasis on the ONE main point.
        ax.text(value + 0.05, y,
                f"{value:.1f}  ← lowest ({gap:.1f} below next)",
                va="center", color=ORANGE, fontweight="bold")
    else:
        ax.text(value + 0.05, y, f"{value:.1f}", va="center")

fig.tight_layout()
st.pyplot(fig, clear_figure=True)

# -------------------------------------------------- explanation (added) ----
# Added label: tells the reader how to read the bars and what "lower" means.
st.markdown(
    "**How to read this chart:** each bar is the *average* self-rating for one "
    "skill (not an individual student's score). A **shorter bar = less "
    "confidence = more support needed.**"
)
st.write(f"**Why it matters:** {frame['why']}")
st.caption("Fictional practice values. Ratings are averages on a 1-5 scale; "
           "not findings from a real survey.")
