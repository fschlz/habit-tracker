import os
import streamlit as st
import datetime as dt
import plotly.express as px
from habit_tracker import data


#######
# HEADER
st.title("💎 Habit Tracker")

dt_now = dt.datetime.now()
dt_str = dt_now.strftime("%Y-%m-%d")
dt_weekday = dt_now.strftime("%A")
dt_day = dt_now.strftime("%-d")
dt_month = dt_now.strftime("%b")

st.markdown(f" Today is {dt_weekday} - {dt_day}. of {dt_month}.")


#######
# SETUP
# load previous config
Pref = data.Preferences()
filepath = Pref.pref_dict.get("data").get("filepath")
filename = Pref.pref_dict.get("data").get("filename")

if (filename in os.listdir(filepath)) and filename.endswith(".csv"):
    habit_data_exists = True
else:
    habit_data_exists = False


#######
# SIDEBAR
st.sidebar.title("Mission Control")

# LOAD/CREATE FILE
sidebar_data_container = st.sidebar.beta_expander(
    "💫 Load or Create a file", expanded=(not habit_data_exists)
)

with sidebar_data_container:
    st.markdown("### 💾 Folder to load from / save to")
    sidebar_folder_path = st.text_input(
        "Choose a folder", value="."
    )

    st.markdown("### 🗂 Load an existing file")
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

    st.markdown("### ✨ or create a new file")

    sidebar_create_file_name = st.text_input(
        "Choose a file name", value="habit_data.csv"
    )
    sidebar_create_file_button = st.button("* Create new file")


# INPUT
sidebar_input_container = st.sidebar.beta_expander(
    "💪🏼 How did you do today?", expanded=habit_data_exists
)

with sidebar_input_container:
    # Choose Date
    sidebar_date = st.date_input(
        "📅 Which day you want to make an entry for?",
        max_value=dt_now
    )

    # Slider Metrics
    sidebar_sleep = st.slider(
        "😴 How much did you sleep?",
        min_value=0.0, max_value=12.0, value=8.0, step=0.1
    )
    sidebar_mood = st.slider(
        "🌈 What mood were you in?",
        min_value=1, max_value=7, value=5, step=1
    )
    sidebar_energy = st.slider(
        "⚡️ How energized did you feel?",
        min_value=1, max_value=7, value=5, step=1
    )

    # Radio Button Metrics
    sidebar_food = st.radio(
        "🥕 Did you eat healthy?", (0, 1)
    )
    sidebar_exercise = st.radio(
        "🏃‍♀️ Did you exercise?", (0, 1)
    )
    sidebar_meditation = st.radio(
        "🧘‍ Did you meditate?", (0, 1)
    )
    sidebar_reading = st.radio(
        "📖 Did you read?", (0, 1)
    )
    sidebar_journaling = st.radio(
        "✏️ Did you journal?", (0, 1)
    )
    sidebar_learning = st.radio(
        "🎓 Did you learn something new?", (0, 1)
    )
    sidebar_work = st.radio(
        "🏆 Did you work towards your goals?", (0, 1)
    )

    # Add data button
    add_row = st.button("➕ Add values")


#######
# DATA
# set file name and folder path
if (sidebar_load_file_name is not None) and (sidebar_create_file_name.endswith(".csv")):
    filepath = sidebar_folder_path
    filename = sidebar_load_file_name

elif sidebar_create_file_button:
    filepath = sidebar_folder_path
    filename = sidebar_create_file_name

elif (habit_data_exists is True) and (sidebar_load_file_name is None):
    st.markdown("🔄 We imported your data from last time")

else:
    st.markdown("### Create or load a file to continue.")
    st.stop()


# LOAD DATA
HabitData = data.HabitData(filepath=filepath, filename=filename)
HabitData.load()

Pref.pref_dict["data"]["filepath"] = filepath
Pref.pref_dict["data"]["filename"] = filename
Pref.save()


# ADD DATA
if add_row:
    append_dict = {
        "date": sidebar_date,
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

    HabitData.add(append_dict=append_dict)


# REMOVE DATA
# add function to sidebar
sidebar_remove_data_container = st.sidebar.beta_expander(
    "🗑 Delete data", expanded=False
)

with sidebar_remove_data_container:
    try:
        opt = HabitData.data.date.unique()
    except AttributeError:
        opt = [None]

    selectbox_remove_date = st.selectbox(
        "Remove data:", options=opt
    )
    drop_row = st.button("➖ Remove values")

if drop_row:
    HabitData.drop(date_index=selectbox_remove_date)


# RELOAD DATA
# reload table after dropping/adding values
HabitData = data.HabitData(filepath=filepath, filename=filename)
HabitData.load()


#######
# VISUALS
# dataframe
data_container = st.beta_expander("Display your data", expanded=True)

with data_container:
    dataframe = st.dataframe(HabitData.data)


# line plot
st.markdown("### Plot your habits over time")

plot_container, info_container = st.beta_columns([8, 2])

with info_container:
    opt = HabitData.data.columns.to_list()
    opt.remove("date")
    selectbox_columns = st.selectbox(
        "Select which column to plot:",
        options=opt
    )

    m = round(HabitData.data[selectbox_columns].mean(), 2)
    metric_dict = {
        "mood": "lvl",
        "energy": "lvl",
        "sleep": "h",
        "food": "%",
        "exercise": "%",
        "meditation": "%",
        "reading": "%",
        "journaling": "%",
        "learning": "%",
        "work": "%",
    }
    # {metric_dict.get(selectbox_columns)}
    st.markdown(f"""# mean // {m}""")

with plot_container:
    px_chart = px.bar(
        HabitData.data,
        x="date", y=selectbox_columns,
        # marginal="box", hover_data=HabitData.data.columns
    )
    st.plotly_chart(px_chart, use_container_width=True)


# # KPIs
# st.markdown("### Here's your average performance")

# mean_container = st.beta_container()  # , current_container = st.beta_columns([1, 1])
# with mean_container:
#     mean_dict = HabitData.data.mean().to_dict()
#     for k, v in mean_dict.items():
#         st.markdown(f"""### {k}:""")
#         st.markdown(f"""# {v}""")

# st.dataframe(pd.DataFrame(HabitData.data.mean().to_dict(), index=[0]))
