import pandas as pd

df = pd.read_csv('flight.csv')

# df = df[df["p1"] == "delhi"]
# df = df[df["p2"] == "mumbai"]
# print(df.head())
# print(df["tkt"].values[0])

df.loc[((df['p1'] == 'ahemdabad') & (df['p2'] == 'delhi')), 'tkt'] = 500
df.to_csv('flight.csv', index=False)