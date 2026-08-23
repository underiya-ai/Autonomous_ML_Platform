import pandas as pd 

df = pd.read_csv("uploads\\encoded\\train_cleaned_encoded.csv")

print(df.head())
print(df.isnull().sum())
print(df.dtypes)
print(df.info())