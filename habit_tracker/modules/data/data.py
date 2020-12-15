import os
import pandas as pd
import json
import base64
from ..helper import helper


class HabitData():
    name = "CRUD Operator for Data"
    description = "Load, save, append, drop or create habit data"

    # def __init__(
    #     self, **kwargs
    # ):

    def load(self, file):
        self.filename = file.name
        data = pd.read_csv(file)
        self.data = data.sort_values(by="date")
        # self.data.set_index("date", inplace=True)

    def add(self, append_dict: dict) -> None:
        self.data = self.data.append(append_dict, ignore_index=True)

    def drop(self, date_index: str) -> None:
        self.data = self.data.drop(
            self.data.loc[self.data.date == date_index].index,
            axis=0
        )

    def create(self, filename: str) -> None:

        df_cols = [
            "date",
            "sleep", "mood", "energy",
            "food", "exercise", "meditation",
            "reading", "journaling", "learning", "work"
        ]

        self.data = pd.DataFrame(columns=df_cols)

        self.filename = helper.check_file_naming(filename, extension=".csv")

    def download(self):
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = self.data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="habit_data.csv">Download habit_data.csv</a>'

        return href

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
