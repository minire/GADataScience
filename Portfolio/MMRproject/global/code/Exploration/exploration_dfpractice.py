# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 18:13:17 2016

@author: minire
"""

import pandas as pd

# creating two data frames to practice concating based on column string 

df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3','A4'], 'B': ['B0', 'B1', 'B2', 'B3','B4'], 'C': ['C0', 'C1', 'C2', 'C3','C4'], 'D': ['D0', 'D1', 'D2', 'D3', 'D4']}, index=[0, 1, 2, 3, 4])
df1


df2 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'], 'E' : ['E0', 'E1', 'E2', 'E3']})
df2

indexed_df1 = df1.set_index(['A'])
indexed_df1

indexed_df2 = df2.set_index(['A'])
indexed_df2

totaldf = pd.concat([indexed_df1, indexed_df2], axis=1)
totaldf

#creating a "wordiness" scale to rate reviews on how much people have written. 

# total length of review as string length 
yelp['wordiness'] = [len(x) for x in yelp['text']]


# defining a scale of 'wordiness' using a list function and list comprehension 
def words(text):
    if len(text) >= 2000:
        return 5 
    elif len(text) >= 1000:
        return 4
    elif len(text) >= 500:
        return 3
    elif len(text) >= 100:
        return 2
    elif len(text) >= 0:
        return 1
    
yelp['word_scale'] = [words(x) for x in yelp ['text']]

