import pandas as pd
import os
from config import DATABASE_PATH

def read_csv(file):
    path = os.path.join(DATABASE_PATH, file)
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

def write_csv(file, data):
    path = os.path.join(DATABASE_PATH, file)
    data.to_csv(path, index=False)