# -*- coding: utf-8 -*-
"""
This script finds how often certain stocks move up or down based on 
day of the week.

The output is a table of the percentage of the time that day ended up green,
sorted by ticker of stocks inputted.
"""

import pandas as pd
import os

# Load in data
dataDir = r'C:\Users\Administrator\Google Drive\Programming\Python\ML_stocks\data'
dataList = os.listdir(dataDir)
tickerList = [x.split(sep='_')[0] for x in dataList]
dataList = [(dataDir + '\\' + x) for x in dataList]

data = pd.DataFrame()
data = [data.append(pd.read_csv(x)) for x in dataList] # makes a list of dataframes
for a in range(len(dataList)):
    data[a]['ticker'] = tickerList[a]

data = pd.concat(data) # concatenates the list of dataframes into one dataframe
data = data.reset_index()
data = data.drop(['index', 'Adj Close'], axis=1)

# Make day of week column
data['day'] = pd.to_datetime(data['Date']).dt.day_name()

# Create column indicating if stock price moved up or down for that day
def which_dir(row):
    if row['Close'] < row['Open']:
        return 0 # price goes down
    else:
        return 1 # price goes up

data['change_dir'] = data[['Close','Open']].apply(which_dir, axis=1)

# Group by day of week
dataGrouped = data.groupby(['ticker','day'])
# Get frequency of price increase for each day
print(dataGrouped.mean()['change_dir'])