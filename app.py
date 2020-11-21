import streamlit as st
import numpy as np
import pandas as pd
import datetime as dt
import plotly.express as px
from habit_tracker import data

#######
# HEADER
st.title("Habit Tracker")

dt_now = dt.datetime.now()
dt_str = dt_now.strftime("%Y-%m-%d")
dt_weekday = dt_now.strftime("%A")
dt_day = dt_now.strftime("%-d")
dt_month = dt_now.strftime("%b")

st.markdown(f" Today is {dt_weekday} - {dt_day}. of {dt_month}.")


#######
# SIDEBAR
st.sidebar.title("How did you do today?")

habit_file = st.sidebar.text_input(
    "where's your data?", value="./habit_tracker/resources/habit_data.csv"
)

# Slider Metrics
sidebar_sleep = st.sidebar.slider(
    "sleep", min_value=0.0, max_value=12.0, value=8.0, step=0.1
)
sidebar_mood = st.sidebar.slider(
    "mood", min_value=1, max_value=7, value=5, step=1
)
sidebar_energy = st.sidebar.slider(
    "energy", min_value=1, max_value=7, value=5, step=1
)

# Radio Button Metrics
sidebar_food = st.sidebar.radio(
    "food", (0, 1)
)
sidebar_exercise = st.sidebar.radio(
    "exercise", (0, 1)
)
sidebar_meditation = st.sidebar.radio(
    "meditation", (0, 1)
)
sidebar_reading = st.sidebar.radio(
    "reading", (0, 1)
)
sidebar_journaling = st.sidebar.radio(
    "journaling", (0, 1)
)
sidebar_learning = st.sidebar.radio(
    "learning", (0, 1)
)
sidebar_work = st.sidebar.radio(
    "work", (0, 1)
)

# Add data button
add_row = st.sidebar.button("+ Add values")


#######
# DATA
df = data.load(filename=habit_file)

# add data
if add_row:
    df_dict = {
        "date": dt_str,
        "mood": sidebar_sleep,
        "energy": sidebar_mood,
        "sleep": sidebar_energy,
        "food": sidebar_food,
        "exercise": sidebar_exercise,
        "meditation": sidebar_meditation,
        "reading": sidebar_reading,
        "journaling": sidebar_journaling,
        "learning": sidebar_learning,
        "work": sidebar_work,
    }

    data.add(df=df, append_dict=df_dict, filename=habit_file)

# remove data
selectbox_date = st.sidebar.selectbox("Remove date:", options=df.date.unique())
drop_row = st.sidebar.button("- Remove values")

if drop_row:
    data.drop(df=df, date_index=selectbox_date, filename=habit_file)

df = data.load(filename=habit_file)


#######
# VISUALS
# dataframe
data_container = st.beta_expander("Display your data", expanded=False)

#data_container, date_select_container = st.beta_columns([3, 1])
with data_container:
    dataframe = st.dataframe(df.style.highlight_max(axis=0, color="lightgreen"))


# line plot
st.markdown("### Plot your habits over time")
graph_container, col_select_container = st.beta_columns([3, 1])

with col_select_container:
    selectbox_columns = st.selectbox(
        "Select which column to plot:",
        options=df.columns.to_list()
    )

with graph_container:
    px_line_chart = px.bar(df, x="date", y=selectbox_columns)
    line_chart = st.plotly_chart(px_line_chart)


# def display_kpis():
#     raise NotImplementedError

# # CRUDdError

# def remove_entry():
#     raise NotImplementedError

# def update_entry():
#     raise NotImplementedError
