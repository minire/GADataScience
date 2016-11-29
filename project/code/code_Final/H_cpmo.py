
import requests
import pandas as pd 
import json
import pickle
import numpy as np

# Creating a function to call script from master 
def getcontra():
        
    # H. grabbing data for contraceptive prevalence - modern methods (%) 'cpmo' 
    # Data in percent (%)
    H = requests.get('http://apps.who.int/gho/athena/api/GHO/cpmo.json')    
    
    # Converting data into json format
    data = H.json()
    data.keys()    
    
    # Creating a data frame that contains the numeric values for cpmo  
    fact = data['fact']
    contrafact = pd.DataFrame(fact)   
    contrafact.value[0]
    contrafact.Dim[0]
    
    # Extracting 'value' from the cpmofact dataframe
    data8 = list(contrafact.value)
    values = pd.DataFrame(data=data8)
    values.head()
    
    # Concat values onto the cpmofact data frame 
    contrafact = pd.concat([contrafact, values], axis=1)
    contrafact.head()
    
    # Pulling the country names, region, and year out of cpmofact['Dim'] column
    def extract(x):
        for col in x:
            if col['category'] == 'COUNTRY':
                return col['code'] 
        
    contrafact['ISO'] = [extract(row) for row in contrafact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'YEAR':
                return col['code'] 
        
    contrafact['contraYEAR'] = [extract(row) for row in contrafact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'REGION':
                return col['code'] 
        
    contrafact['REGION'] = [extract(row) for row in contrafact['Dim']]    
    
    # Removing uneccessary feature columns
    contrafact.drop(['Dim', 'dataset', 'comments', 'effective_date', 'end_date', 'fact_id', 'published', 'value', 'display', 'high', 'low'], axis=1, inplace=True)
    
    # Renamning data frame     
    contra = contrafact
    #contra.head()
    contra.describe()
    #contra.dtypes
    
    # Looking at null values
    null_data = contra[contra.isnull().any(axis=1)]
    #print null_data
    
    # Removing null values 
    contra = contra[contra.ISO.notnull()]
    contra = contra[contra.numeric.notnull()]
    
    # Converting year to numeric
    contra.loc[:, 'contraYEAR'] = pd.to_numeric(contra.loc[:, 'contraYEAR'])
    contra.describe()
    
    # Sorting by year and then country three letter code
    CY = contra.sort_values(['contraYEAR'],ascending=False)
    CYN = CY.drop_duplicates('ISO', keep = 'first' ).values
    
    # Create a cellphone subscription data frame, drop unecessary columns, set index to ISO 
    contra = pd.DataFrame(data=CYN)
    contra = contra.rename(columns = {0 : 'contraceptives%', 1 : 'ISO', 2 : 'contraYEAR', 3 : 'REGION'})
    contra.drop(['REGION'], axis=1, inplace=True) 
    
    # Converting columns to numeric 
    contra[['contraceptives%', 'contraYEAR']] = contra[['contraceptives%', 'contraYEAR']].astype(float)
    
    return contra