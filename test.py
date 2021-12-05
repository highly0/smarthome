import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import pathlib

app_path = str(pathlib.Path(__file__).parent.resolve())
#the data smarthome.csv
df = pd.read_csv(os.path.join(app_path, os.path.join("data", "HomeC.csv")))

app = Dash(__name__, url_base_pathname='/dashboard/')
keep_col = ['time','dishwasher_[kw]','fridge_[kw]','garage_door_[kw]','microwave_[kw]']

#cleaning
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

new_f = df[keep_col]
df.drop(index=df.index[-:], axis=0, inplace=True)
new_f.to_csv("newFile.csv", index=False)
print(df.columns)