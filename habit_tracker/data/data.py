import pandas as pd

def load():
    df = pd.read_csv("./habit_tracker/resources/habit_data.csv")
    # df.date = pd.to_datetime(df.date, format="%Y-%m-%d")
    return df

def add(df, append_dict):
    df = df.append(append_dict, ignore_index=True)
    df.to_csv("./habit_tracker/resources/habit_data.csv", index=False)

def drop(df, date_index):
    df = df.drop(df.loc[df.date==date_index].index, axis=0)
    df.to_csv("./habit_tracker/resources/habit_data.csv", index=False)