#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 21:42:43 2017

@author: valiantswabian
"""
import pandas as pd
import matplotlib.pyplot as plt
import sys # this is to know the python version
import matplotlib

#matplotlib inline

print ('Python version : ' + sys.version)
print ('Pandas version : ' + pd.__version__)
print ('Matplotlib version : ' + matplotlib.__version__)

# create some data
names = ['Bob','Jessica','Mary','John','Mel']
births = [968, 155, 77, 578, 973]

# making a list of baby names and birthrates
BabyDataSet = list(zip(names,births))

df = pd.DataFrame(data = BabyDataSet, columns=['names','births'])

# export it as csv
Location = r'/Volumes/ValiantSwabian/Deep_Learning/Machine_Learning_nD/Pandas_101/baby_birthrate.csv'
df.to_csv(Location, index=False, header=False)
# if header argument is not provided then read_csv treats first row as header
# we can give names like below or turn the header argument to true
df = pd.read_csv(Location, names=['names','births'])

import os
os.remove(Location)

# Next we check the datatypes of the columns
df.dtypes
df.births.dtype

# Find the most popular baby name following two approaches
# - Sort the dataframe and select top row or
# - Use the max() attribute to find the max value
Sorted = df.sort_values(['births'], ascending=False)
Popular_name = Sorted.head(1).values
# method 2
               
# make it visible
df['births'].plot()
MaxVal = df['births'].max()
Popular_name2 = df['names'][df['births'] == df['births'].max()].values

Text = str(MaxVal) + " - " + Popular_name2
plt.annotate(Text,xy=(1,MaxVal),xytext=(8,0),
             xycoords=('axes fraction','data'),
             textcoords='offset points')
#plt.xticks(df['names'], rotation = 0)
plt.title('The most popular name')
plt.xlabel('Names')
plt.ylabel('Frequency')
plt.legend()
plt.show()                      





