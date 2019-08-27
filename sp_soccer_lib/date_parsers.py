import pandas as pd


def dateparser1819(x):
    return pd.datetime.strptime(x, "%d/%m/%Y")


def dateparser1718(x):
    return pd.datetime.strptime(x, "%d/%m/%y")
