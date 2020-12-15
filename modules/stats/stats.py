import pandas as pd
from ..data import data
from ..helper import helper


class KPIs():
    name = "Key Performance Indicators of Habit Data"
    drescription = "Calculate KPIs based on Habit Data"

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.get_kpis()

    def get_kpis(self):
        raise NotImplementedError

    def performance_index(self):
        max_sum = 28
        self.data.set_index("date").sum(axis=1).div(max_sum)
        raise NotImplementedError


class HabitPredictor():
    name = "ML for Habit Data"
    drescription = "Calculate predictions based on Habit Data"

    def __init__(self, data: pd.DataFrame):
        self.data = data
