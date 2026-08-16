import pandas as pd 
import numpy as np 

print("="*200)
df = pd.read_csv("uploads/cleaned/train_cleaned.csv")
print(df.head())
print(df.tail())
print(df.columns)
print(df.info())