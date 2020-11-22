import os
import streamlit as st
import datetime as dt
import plotly.express as px
from habit_tracker import data

#######
# SETUP
# load previous config
pref_dict = data.load_preferences()
filepath = pref_dict.get("data").get("filepath")
filename = pref_dict.get("data").get("filename")

if (filename in os.listdir(filepath)) and filename.endswith(".csv"):
    habit_data_exists = True
    file = os.path.join(filepath, filename)
else:
    habit_data_exists = False


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
st.sidebar.title("Mission Control")

# LOAD/CREATE FILE
sidebar_data_container = st.sidebar.beta_expander(
    "Load or Create a file", expanded=False
)

with sidebar_data_container:
    st.markdown("### Folder you want to load/save data to")
    sidebar_folder_path = st.text_input(
        "Choose a folder", value="."
    )

    st.markdown("### Load an existing file")
    try:
        sidebar_load_file_name = st.selectbox(
            "Choose a file", options=[None]+os.listdir(sidebar_folder_path)
        )
    except FileNotFoundError:
        st.markdown(
            f"""❌ <b>EEEHHHHT!</b>
            <br>🤔 That directory does not exist.
            <br>Please type in an existing directory
            <br>
            <br>Here is a list of items in your current working directory:
            <br><i>{os.listdir(".")}</i>
            """,
            unsafe_allow_html=True
        )
        st.stop()

    st.markdown("### or create a new file")

    sidebar_create_file_name = st.text_input(
        "Choose a file name", value="habit_data.csv"
    )
    sidebar_create_file_button = st.button("* Create new file")


# INPUT
sidebar_input_container = st.sidebar.beta_expander(
    "How did you do today?", expanded=False
)

with sidebar_input_container:
    # Choose Date
    sidebar_date = st.date_input(
        "Which day you want to make an entry for?",
        max_value=dt_now
    )

    # Slider Metrics
    sidebar_sleep = st.slider(
        "How much did you sleep?",
        min_value=0.0, max_value=12.0, value=8.0, step=0.1
    )
    sidebar_mood = st.slider(
        "What mood were you in?",
        min_value=1, max_value=7, value=5, step=1
    )
    sidebar_energy = st.slider(
        "How energized did you feel?",
        min_value=1, max_value=7, value=5, step=1
    )

    # Radio Button Metrics
    sidebar_food = st.radio(
        "Did you eat healthy?", (0, 1)
    )
    sidebar_exercise = st.radio(
        "Did you exercise?", (0, 1)
    )
    sidebar_meditation = st.radio(
        "Did you meditate?", (0, 1)
    )
    sidebar_reading = st.radio(
        "Did you read?", (0, 1)
    )
    sidebar_journaling = st.radio(
        "Did you write in your journal?", (0, 1)
    )
    sidebar_learning = st.radio(
        "Did you learn somethign new?", (0, 1)
    )
    sidebar_work = st.radio(
        "Did you work towards your goals?", (0, 1)
    )

    # Add data button
    add_row = st.button("+ Add values")


#######
# DATA
abs_folderpath = os.path.abspath(sidebar_folder_path)

if (sidebar_load_file_name is not None) and (sidebar_create_file_name.endswith(".csv")):
    file = os.path.join(abs_folderpath, sidebar_load_file_name)
    df = data.load(filename=file)

    pref_dict["data"]["filepath"] = abs_folderpath
    pref_dict["data"]["filename"] = sidebar_load_file_name
    data.save_preferences(pref_dict)

elif sidebar_create_file_button:
    file = os.path.join(abs_folderpath, sidebar_create_file_name)
    df = data.create(filename=file)

    pref_dict["data"]["filepath"] = abs_folderpath
    pref_dict["data"]["filename"] = sidebar_create_file_name
    data.save_preferences(pref_dict)

elif (habit_data_exists is True) and (sidebar_load_file_name is None):
    df = data.load(filename=file)



else:
    st.markdown("### Create or load a file to continue.")
    st.stop()


# ADD DATA
# add data logic
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

    data.add(df=df, append_dict=df_dict, filename=file)


# REMOVE DATA
# add function to sidebar
sidebar_remove_data_container = st.sidebar.beta_expander(
    "Delete data", expanded=False
)

with sidebar_remove_data_container:
    try:
        opt = df.date.unique()
    except AttributeError:
        opt = [None]

    selectbox_remove_date = st.selectbox(
        "Remove data:", options=opt
    )
    drop_row = st.button("- Remove values")

# remove data logic
if drop_row:
    data.drop(
        df=df,
        date_index=selectbox_remove_date,
        filename=file
    )


# RELOAD DATA
# reload table after dropping/adding values
df = data.load(filename=file)


#######
# VISUALS
# dataframe
data_container = st.beta_expander("Display your data", expanded=False)

# data_container, date_select_container = st.beta_columns([3, 1])
with data_container:
    dataframe = st.dataframe(df)


# line plot
st.markdown("### Plot your habits over time")
graph_container, col_select_container = st.beta_columns([3, 1])

with col_select_container:
    opt = df.columns.to_list()
    opt.remove("date")
    selectbox_columns = st.selectbox(
        "Select which column to plot:",
        options=opt
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
