import pandas as pd

def load_data(data_path):
    return pd.read_csv(data_path)

def categorize(df, column):
    """
    Categorizes the values of a given column

    Args:
        df (pd.DataFrame): Dataframe containing data
        column (str): Column to categorize

    Returns:
        pd.DataFrame: Categorized Dataframe
    """

    df = df.copy()
    df[column] = df[column].astype('category')
    return df


def add_notnull_variable(df, column, new_column = None):
    """
    Creates a Boolean variable that evaluates
    missing values
    """

    df = df.copy()

    if new_column is None:
        new_column = f'has_{column}'

    df[new_column] = df[column].notna()

    return df