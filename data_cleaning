import pandas as pd

dane = pd.read_excel('dane_projekt.xls')
print(dane.head())

summary = dane.describe()
print(summary)

#brakujące obserwacje
missing = dane.isnull()
print(missing.sum())

data_cleaned = dane.dropna()
#zapis do csv
data_cleaned.to_csv('dane.csv', index=False)