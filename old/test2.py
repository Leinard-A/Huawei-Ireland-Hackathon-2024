import pandas as pd
import numpy as np
import uuid

df = pd.read_csv('data/nba.csv')

indexAge = df[df['Age'] >= 25].index
df.drop(indexAge)
print(df)