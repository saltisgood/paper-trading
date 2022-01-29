from pandas import DataFrame


def rows_count(df: DataFrame):
    return len(df.index)
