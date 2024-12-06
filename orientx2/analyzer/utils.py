import pandas as pd


def load_data(csv_file):
    df = pd.read_csv(csv_file)
    df['date'] = pd.to_datetime(df['date'])
    return df


def add_day_index(df, start_date):
    df['day_index'] = (df['date'] - pd.Timestamp(start_date)).dt.days
    return df


def prepare_orientation_data(df, graph_label):
    df['orientation'] = (df['orientation'] == graph_label)
    return df
