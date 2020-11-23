import os
import pandas as pd
import json
from ..helper import helper


class HabitData():
    name = "CRUD Operator for Data"
    description = "Load, save, append, drop or create habit data"

    def __init__(
        self,
        filepath: str,
        filename: str,
        **kwargs
    ):
        self.file = os.path.join(os.path.abspath(filepath), filename)

    def load(self):
        data = pd.read_csv(self.file)
        self.data = data.sort_values(by="date")

    def save(self):
        self.data.to_csv(self.file, index=False)

    def add(self, append_dict: dict) -> None:
        self.data = self.data.append(append_dict, ignore_index=True)
        self.save()

    def drop(self, date_index: str) -> None:
        self.data = self.data.drop(
            self.data.loc[self.data.date == date_index].index,
            axis=0
        )
        self.save()

    def create(self) -> None:

        df_cols = [
            "date",
            "sleep", "mood", "energy",
            "food", "exercise", "meditation",
            "reading", "journaling", "learning", "work"
        ]

        self.data = pd.DataFrame(columns=df_cols)

        self.file = helper.check_file_naming(self.file, extension=".csv")

        self.save()

    @staticmethod
    def get_append_dict() -> dict:

        col_dict = {
            "date": "",
            "mood": "",
            "energy": "",
            "sleep": "",
            "food": "",
            "exercise": "",
            "meditation": "",
            "reading": "",
            "journaling": "",
            "learning": "",
            "work": "",
        }

        return col_dict


class Preferences():
    name = "Preferences Operator"
    description = "Load preferences as a Dict or Save preferences as JSON"

    def __init__(
        self,
        filepath: str = "./habit_tracker/config",
        filename: str = "preferences.json",
        **kwargs
    ):

        self.filepath = os.path.abspath(filepath)
        self.filename = filename

        self.file = os.path.join(self.filepath, self.filename)

        self.load()

    def load(self) -> None:
        with open(self.file, "r") as f:
            self.pref_dict = json.load(f)

    def update(self, update_dict: dict) -> None:
        filepath = os.path.abspath(update_dict.get("data").get("filepath"))
        self.pref_dict["data"]["filepath"] = filepath
        self.pref_dict["data"]["filename"] = update_dict.get("data").get("filename")
        self.save()

    def save(self) -> None:
        with open(self.file, "w") as f:
            json.dump(self.pref_dict, f, indent=4)
