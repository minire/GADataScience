
import requests
import pandas as pd 
import json
import pickle
import numpy as np

# Creating a function to call script from master 
def getattend():
    
    # I. Grabbing data for births attended by skilled health personnel (%) 'MDG_0000000025'
    # Data in percent (%)
    I = requests.get('http://apps.who.int/gho/athena/api/GHO/MDG_0000000025.json')   
   
    # Converting data into json format
    data = I.json()
    data.keys()    
    
    # Creating a data frame that contains the fact key of the dataset  
    fact = data['fact']
    attendfact = pd.DataFrame(fact)   
    attendfact.value[0]
    attendfact.Dim[0]
    attendfact.head()
    
    # Extracting 'value' from the attendfact dataframe
    data9 = list(attendfact.value)
    values = pd.DataFrame(data=data9)
    values.head()
    
    # Concat values onto the attendfact data frame 
    attendfact = pd.concat([attendfact, values], axis=1)
    attendfact.head()
    
    # Pulling the country names, region, and year out of attendfact['Dim'] column 
    def extract(x):
        for col in x:
            if col['category'] == 'COUNTRY':
                return col['code'] 
        
    attendfact['ISO'] = [extract(row) for row in attendfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'YEAR':
                return col['code'] 
        
    attendfact['attendYEAR'] = [extract(row) for row in attendfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'REGION':
                return col['code'] 
        
    attendfact['REGION'] = [extract(row) for row in attendfact['Dim']]    
    
    # Removing uneccessary feature columns
    attendfact.drop(['Dim', 'dataset', 'comments', 'effective_date', 'end_date', 'fact_id', 'published', 'value', 'display', 'high', 'low'], axis=1, inplace=True)
    
    # Renamning data frame     
    attend = attendfact
    #attend.head()
    #attend.dtypes
    #attend.describe()  
    
    # Looking at null values
    null_data = attend[attend.isnull().any(axis=1)]
    #print null_data
    
    # Removing null values 
    attend = attend[attend.ISO.notnull()]
    
    # Checking for duplicate countries in the data set 
    attend.shape
    duplicates = attend.groupby(attend['ISO']).sum() 
    print duplicates[duplicates['numeric'] == 1]
    
    # Standardizing year format
    def stdYEAR(year):
        for character in year:
            return year[0:4]
                
    attend['attendYEAR']=[stdYEAR(row) for row in attend['attendYEAR']]
    
    # Converting year to numeric removing region feature 
    attend['attendYEAR'] = pd.to_numeric(attend['attendYEAR'], errors='coerce') 
    attend.drop(['REGION'], axis=1, inplace=True) 
    
    # Renaming and converting columns to numeric
    attend = attend.rename(columns = {'numeric' : 'attend%' })
    attend[['attend%', 'attendYEAR']] = attend[['attend%', 'attendYEAR']].astype(float)
    
    
    return attend