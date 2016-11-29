
import requests
import pandas as pd 
import json
import pickle
import numpy as np

# Creating a function to call script from master 
def gethomicide():
        
    # K. Grabbing data for estimates of rates of homicide 'VIOLENCE_HOMICIDERATE'
    # Per 100 000 population     
    K = requests.get('http://apps.who.int/gho/athena/api/GHO/VIOLENCE_HOMICIDERATE.json')   
   
    # Converting data into json format
    data = K.json()
    data.keys()    
    
    # Creating a data frame that contains homicides per 100K people (homicide)   
    fact = data['fact']
    homicidefact = pd.DataFrame(fact)   
    homicidefact.value[0]
    homicidefact.Dim[0]
    
    # Extracting 'value' from the homicidefact dataframe
    data11 = list(homicidefact.value)
    values = pd.DataFrame(data=data11)
    values.head()
    
    # Concat values onto the homicidefact data frame 
    homicidefact = pd.concat([homicidefact, values], axis=1)
    homicidefact.head()
    
    # Pulling the country names, region, and year out of homicidefact['Dim'] column   
    def extract(x):
        for col in x:
            if col['category'] == 'COUNTRY':
                return col['code'] 
        
    homicidefact['ISO'] = [extract(row) for row in homicidefact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'YEAR':
                return col['code'] 
        
    homicidefact['homicideYEAR'] = [extract(row) for row in homicidefact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'REGION':
                return col['code'] 
        
    homicidefact['REGION'] = [extract(row) for row in homicidefact['Dim']]
    
    # Removing uneccessary feature columns
    homicidefact.drop(['Dim', 'dataset', 'effective_date', 'end_date', 'fact_id', 'published', 'value', 'display', 'high', 'low'], axis=1, inplace=True)
    
    # Renamning data frame     
    homicide = homicidefact
    #homicide.head()
    homicide.describe()
    #homicide.dtypes
    
    # Looking at null values
    null_data = homicide[homicide.isnull().any(axis=1)]
    print null_data
    
    # Removing null values 
    #homicide = homicide[homicide.ISO.notnull()]
    #homicide = homicide[homicide.numeric.notnull()]
    
    # Converting year to numeric
    homicide.loc[:, 'homicideYEAR'] = pd.to_numeric(homicide.loc[:, 'homicideYEAR'])
        
    # Sorting by year and then country three letter code
    HY = homicide.sort_values(['homicideYEAR'],ascending=False)
    HYN = HY.drop_duplicates('ISO', keep = 'first' ).values
    
    # Create a cellphone subscription data frame, drop unecessary columns, set index to ISO 
    homicide = pd.DataFrame(data=HYN)
    homicide = homicide.rename(columns = {0 : 'homicide100K', 1 : 'ISO', 2 : 'homicideYEAR', 3 : 'REGION'})
    homicide.drop(['REGION'], axis=1, inplace=True) 
    
    # Converting to columns to numeric 
    homicide[['homicide100K', 'homicideYEAR']] = homicide[['homicide100K', 'homicideYEAR']].astype(float)
    
    return homicide