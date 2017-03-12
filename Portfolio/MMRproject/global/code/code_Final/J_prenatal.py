import requests
import pandas as pd 
import json
import pickle
import numpy as np

# Creating a function to call script from master 
def getPrenat():
    
    # J. grabbing data for antenatal care coverage - at least four visits (%) 'whs4_154': 
    # Data as a percent (%)
    J = requests.get('http://apps.who.int/gho/athena/api/GHO/whs4_154.json')    
    
    # Converting data into json format
    data = J.json()
    data.keys()    
    
    # Creating a data frame that contains percent of mothers with at least four prenatal visits   
    fact = data['fact']
    prenatfact = pd.DataFrame(fact)   
    prenatfact.value[0]
    prenatfact.Dim[0]
    prenatfact.head()
    
    # Extracting 'value' from the prenatfact dataframe
    data10 = list(prenatfact.value)
    values = pd.DataFrame(data=data10)
    values.head()    
    
    # Concat values onto the prenatfact data frame 
    prenatfact = pd.concat([prenatfact, values], axis=1)
    prenatfact.head()
    
    # Pulling the country names, region, and year out of prenatfact['Dim'] column     
    def extract(x):
        for col in x:
            if col['category'] == 'COUNTRY':
                return col['code'] 
        
    prenatfact['ISO'] = [extract(row) for row in prenatfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'YEAR':
                return col['code'] 
        
    prenatfact['prenatYEAR'] = [extract(row) for row in prenatfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'REGION':
                return col['code'] 
        
    prenatfact['REGION'] = [extract(row) for row in prenatfact['Dim']]    

    # Removing uneccessary feature columns
    prenatfact.drop(['Dim', 'dataset', 'comments', 'effective_date', 'end_date', 'fact_id', 'published', 'value', 'display', 'high', 'low'], axis=1, inplace=True)
    
    # Renamning data frame     
    prenat = prenatfact
    #prenat.head()
    #prenat.dtypes
    #prenat.describe()    
        
    # Looking at null values
    null_data = prenat[prenat.isnull().any(axis=1)]
    #print null_data    

    # Removing null values 
    prenat = prenat[prenat.ISO.notnull()]
    prenat.describe()    
    
    # Standardizing year format
    #print prenat.groupby(prenat['prenatYEAR']).count()    
    def stdYEAR(year):
        for character in year:
            return year[0:4]       
                          
    prenat['prenatYEAR']=[stdYEAR(row) for row in prenat['prenatYEAR']]    
    
    # Converting year to numeric
    prenat['prenatYEAR'] = pd.to_numeric(prenat['prenatYEAR'], errors='coerce')    
    
    # Sorting by year and then country three letter code
    PY = prenat.sort_values(['prenatYEAR'],ascending=False)
    PYN= PY.drop_duplicates('ISO', keep = 'first' ).values
    
    # Create a prenatal care data frame by most recent year, drop unecessary columns, set index to ISO 
    prenat = pd.DataFrame(data=PYN)
    prenat = prenat.rename(columns = {0 : 'prenat%', 1 : 'ISO', 2 : 'prenatYEAR', 3 : 'REGION'})
    prenat.drop(['REGION'], axis=1, inplace=True) 
    
    # Converting columns to numeric 
    prenat[['prenat%', 'prenatYEAR']] = prenat[['prenat%', 'prenatYEAR']].astype(float)
    #prenat.describe()

    return prenat