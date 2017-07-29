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

# create a data base with 1000 names using these names
Database_entries = 1000
random.seed(0)
random_names = [names[random.randint(low=0,high=len(names))] 
                for i in range(Database_entries)]

births = [random.randint(low=0, high=1000)
          for i in range(Database_entries)]

# making a list of baby names and birthrates
BabyDataSet = list(zip(random_names,births))

df = pd.DataFrame(data = BabyDataSet, columns=['names','births'])

# export it as csv
# slashes are special characters, 
# prefixing the string with a r will escape the whole string.
Location = r'/Volumes/ValiantSwabian/Deep_Learning/Machine_Learning_nD/Pandas_101/baby_birthrate.csv'
df.to_csv(Location, index=False, header=False)
# if header argument is not provided then read_csv treats first row as header
# we can give names like below or turn the header argument to true
df = pd.read_csv(Location, names=['names','births'])
# info provides a summary of dataset
df.info()
df.head(5)
df.tail(5)
# once we are done with csv this removes it
import os
os.remove(Location)

# Next we check the datatypes of the columns
df.dtypes
df.births.dtype

# find unique names
df['names'].unique()
for i in df['names'].unique():
    print(i)
# 
print (df['names'].describe())

# Next we know we have only 5 unique data points
# We need to "group" 1000 rows into 5 rows
# also add their birthrates when we group 
unique_name = df.groupby('names')#['births'].sum()
df = unique_name.sum()

# Find the most popular baby name following two approaches
# - Sort the dataframe and select top row or
# - Use the max() attribute to find the max value
Sorted = df.sort_values(['births'], ascending=False)
Popular_name = Sorted.head(1).values
# method 2
               
# make it visible
df['births'].plot.bar()
MaxVal = df['births'].max()
#Popular_name2 = df['names'][df['births'] == df['births'].max()].values

#Text = str(MaxVal) + " - " + Popular_name
#plt.annotate(Text,xy=(1,MaxVal),xytext=(8,0),
#             xycoords=('axes fraction','data'),
#             textcoords='offset points')
#plt.xticks(df['names'], rotation = 0)
plt.title('The most popular name')
plt.xlabel('Names')
plt.ylabel('Frequency')
plt.legend()
plt.show()                      





