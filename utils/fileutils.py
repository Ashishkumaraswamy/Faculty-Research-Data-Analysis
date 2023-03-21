import pandas as pd
import numpy as np
import os

CWD = os.path.abspath('.')
PARENT_DIR = os.path.dirname(CWD)
DATA_FOLDER = "Research_Area_Analysis_AMCS/data"


def store_csv(df, name):
    df.to_csv(PARENT_DIR.replace(
        '\\', '/')+'/data/{}.csv'.format(name), index=False, header=True)
