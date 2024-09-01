import pandas as pd
import numpy as np


def reward(row):
    if row['age'] >= 90:
        return row['fav_food']
    if (row['time_in_bed'] > 5) & (row['pct_sleeping'] > 0.5):
        return row['fav_food']
    return['hate_food']


def getData(size=10000):
    df = pd.DataFrame()
    df['age'] = np.random.randint(0, 100, size)
    df['time_in_bed'] = np.random.randint(0, 9, size)
    df['pct_sleeping'] = np.random.rand(size)
    df['fav_food'] = np.random.choice(['pizza', 'burger', 'chips'], size)
    df['hate_food'] = np.random.choice(['peas', 'carrots', 'apples'], size)
    return df

# Level 1
df = getData()

for i, row in df.iterrows():
    df.loc[i, 'reward'] = reward(row)

print('done1')

# Level 2
df = getData()
df['reward'] = df.apply(reward, axis = 1)
print('done2')

# Level 3
df = getData()
df['reward'] = df['hate_food']
df.loc[((df['pct_sleeping'] > 0.5) &
        (df['time_in_bed'] > 5)) |
        (df['age'] > 90), 'reward'] = df['fav_food']

print('done3')
