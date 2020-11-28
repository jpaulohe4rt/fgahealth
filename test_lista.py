import pandas as pd
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("datasets").resolve()
df_global = pd.read_excel(DATA_PATH.joinpath("covid_global_trans.xlsx"))

new_end_date_df1 = df_global[df_global.date == '22/08/2020']


df = new_end_date_df1.values.tolist()

for i in range(len(df)):
    for h in range(0, len(df)-i-1 ):
        if df[h][6] < df[h+1][6]:
            df[h], df[h+1] = df[h+1], df[h]
for i in range(len(df)):
    if df[i][2] == "Mundo":
        df[i] = None 

print(df[0:4])
