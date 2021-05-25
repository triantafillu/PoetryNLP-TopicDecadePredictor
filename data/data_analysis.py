import pandas as pd

df = pd.read_json(open("result92.json", "r", encoding="utf8"))

print(df.info())
print('\n')
print(df.describe())
print('\n')
print(df.isna().sum())
print('\n')
print(df[df.themes.isna()])