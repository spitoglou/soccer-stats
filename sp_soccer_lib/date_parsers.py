# import pandas as pd
from datetime import datetime


def dateparser1819(x):
    return datetime.strptime(x, "%d/%m/%Y")


def dateparser1718(x):
    return datetime.strptime(x, "%d/%m/%y")
