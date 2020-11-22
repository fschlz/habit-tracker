import os
import pandas as pd
import json
import streamlit as st
from ..helper import helper

# TODO: put this into a Data class
def load(filename):
    df = pd.read_csv(filename)
    # df.date = pd.to_datetime(df.date, format="%Y-%m-%d")
    return df


def add(df, append_dict, filename):
    df = df.append(append_dict, ignore_index=True)
    df.to_csv(filename, index=False)


def drop(df, date_index, filename):
    df = df.drop(df.loc[df.date == date_index].index, axis=0)
    df.to_csv(filename, index=False)


def create(filename):

    df_cols = [
        "date",
        "sleep",
        "mood",
        "energy",
        "food",
        "exercise",
        "meditation",
        "reading",
        "journaling",
        "learning",
        "work"
    ]

    df = pd.DataFrame(columns=df_cols)

    filename = helper.check_filename(filename, extension=".csv")

    df.to_csv(filename, index=False)


def load_preferences():
    # load locally saved json file
    with open("./habit_tracker/config/preferences.json", "r") as file:
        pref = json.load(file)

    return pref


def save_preferences(pref_dict):
    with open("./habit_tracker/config/preferences.json", "w") as file:
        json.dump(pref_dict, file, indent=4)
