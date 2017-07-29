#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 12:12:19 2017

@author: valiantswabian
"""
# Import all libraries needed for the tutorial
import pandas as pd
from numpy import random
import matplotlib.pyplot as plt
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number
import numpy.random as np

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)

# set seed
np.seed(0)

# Function to generate test data
def CreateDataSet(Number=1):
    Output = []
    DataSize = 1000
    for i in range(Number):
        # Create a weekly (mondays) date range
        rng = pd.date_range(start='1/1/2009', 
                            end='12/31/2012', 
                            freq='W-MON')
        # Create random data
        data = np.randint(low=25,high=DataSize,size=len(rng))
        # Status pool
        status = [1,2,3]
        # Make a random list of statuses
        random_status = [status[np.randint(low=0,high=len(status))] 
                         for i in range(len(rng))]
        # State pool
        states = ['GA','FL','fl','NY','NJ','TX']
        # Make a random list of states 
        random_states = [states[np.randint(low=0,high=len(states))] 
                         for i in range(len(rng))]
        Output.extend(zip(random_states, random_status, data, rng))
    return Output

dataset = CreateDataSet(4)
df = pd.DataFrame(data=dataset, columns=['State','Status',
                                         'CustomerCount',
                                         'StatusDate'])
df.info()

# save the df to excel
df.to_excel('Customer_data.xlsx', index=False)
Location = r'/Volumes/ValiantSwabian/Deep_Learning/Machine_Learning_nD/Pandas_101/Customer_Data.xlsx'
df = pd.read_excel(Location, 0, index_col='StatusDate')
df.dtypes
df.index

# Cleaning the data for analysis
"""
    1) Make sure 'State' column in  all in upper case
    2) Onlt select records where the count of status = 1
    3) Merge NJ and NY to NY state column
    4) Remove outliers
"""
# Update state column and convert to upper case
df['State'] = df.State.apply(lambda x: x.upper())
# filter by 'Status' == 1
mask = df['Status'] == 1
df = df[mask]
# To merger NJ and NY into NY, just replace all NJ to NY
mask = df['State'] == 'NJ'
df['State'][mask] = 'NY'
    
df['CustomerCount'].plot(figsize=(15,4))

# we have duplicate rows so we group them. We will also add the other attributes
# we will also index them by stat and status date now
Daily = df.reset_index().groupby(['State','StatusDate']).sum()
# Index would include two levels, State, StatusDate
Daily.index
# Index per state
Daily.index.levels[0]
# Index per status date
Daily.index.levels[1]  


# keeping status column is redundant now, it is all the same
del Daily['Status']
# Plot the data per state
for i in df['State'].unique():
    Daily.loc[i].plot()
    plt.title('Customer Count for State of ' + str(i))

# Plot the data per specific year 2012
year = 2012
for i in df['State'].unique():
    Daily.loc[i][str(year):].plot()
    plt.title('Customer Count for State of ' 
              + str(i) + " Year " + str(year))
   
# make plots finer grain to months
StateYearMonth = Daily.groupby([Daily.index.get_level_values(0),
                 Daily.index.get_level_values(1).year,
                 Daily.index.get_level_values(1).month])

# Treating/Eliminating Outliers
# lower = Q1 - 1.5 times (IQR) 
# upper = Q3 + 1.5 times (IQR) 
Daily['Q1'] = Daily['Lower'] = StateYearMonth['CustomerCount'].transform(
           lambda x: x.quantile(q=.25))
Daily['Q3'] = Daily['Lower'] = StateYearMonth['CustomerCount'].transform(
           lambda x: x.quantile(q=.75))
Daily['IQR'] = Daily['Lower'] = StateYearMonth['CustomerCount'].transform(
           lambda x: 1.5*x.quantile(q=.75) - x.quantile(q=.25))
   
Daily['Lower'] = Daily['Q1'] - Daily['IQR']
Daily['Upper'] = Daily['Q3'] + Daily['IQR']

Daily['Outliers'] = ((Daily['CustomerCount'] < Daily['Lower']) |
                    (Daily['CustomerCount'] > Daily['Upper']))

# Remove outliers from Database
# Keep only those with False
Daily = Daily[Daily['Outliers'] == False]

# Create a separate dataframe named ALL
# group Daily df by StatusDate
# get rid of State column
# do another max colum showing max number of customer count
DailyA = pd.DataFrame(Daily['CustomerCount'].groupby(
                        Daily.index.get_level_values(1)).sum())

# Now we group by year and month
YearMonth = DailyA.groupby([lambda x: x.year, lambda x: x.month])

# Max customer per year and month
DailyA['Max'] = YearMonth['CustomerCount'].transform(lambda x: x.max())
# Ploting ALL marckets
DailyA['Max'].plot(figsize=(10, 5));plt.title('ALL Markets')

# See if the customercount meets the expectation
# Create BHAG a.k.a. Big Hairy Annual Goal data frame
data = [1000,2000,3000]
idx = pd.date_range(start='12/31/2011',end='12/31/2013',freq='A') # Annual
BHAG = pd.DataFrame(data, index=idx, columns=['BHAG'])

# Combine the dataframes using concat function
combined = pd.concat([DailyA , BHAG], axis=0)

# Visualizing
fig, axes = plt.subplots(figsize=(12, 7))
combined['BHAG'].fillna(method='pad').plot(color='green', label='BHAG')
combined['Max'].plot(color='blue', label='All Markets')
plt.legend(loc='best');

Year = combined.groupby(lambda x: x.year).max()
# Add a column showing percentage change per year
Year['YR_PCT_Change']=Year['Max'].pct_change(periods=1)
# Predicting next year assuming constant growth
(1 + Year.ix[year,'YR_PCT_Change']) * Year.ix[year,'Max']

