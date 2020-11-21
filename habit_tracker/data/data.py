import pandas as pd


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
