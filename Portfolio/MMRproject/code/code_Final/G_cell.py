
import requests
import pandas as pd 
import json
import pickle
import numpy as np

# Creating a function to call script from master 
def getCell():
    
    # G. Grabbing data for cellular subscribers (per 100 population) 'WHS9_CS'
    # Data given as a percent (%)
    G = requests.get('http://apps.who.int/gho/athena/api/GHO/WHS9_CS.json')    
    
    # Converting data into json format
    data = G.json()
    data.keys()    
    
    # Creating a data frame that contains Cellular subscribers  (cell)  
    fact = data['fact']
    cellfact = pd.DataFrame(fact)   
    cellfact.value[0]
    cellfact.Dim[0]
    
    # Extracting 'value' from the cellfact dataframe
    data7 = list(cellfact.value)
    values = pd.DataFrame(data=data7)
    values.head()
    
    # Concat values onto the cellfact data frame 
    cellfact = pd.concat([cellfact, values], axis=1)
    cellfact.head()
    
    # Pulling the country names, region, and year out of cellfact['Dim'] column   
    def extract(x):
        for col in x:
            if col['category'] == 'COUNTRY':
                return col['code'] 
        
    cellfact['ISO'] = [extract(row) for row in cellfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'YEAR':
                return col['code'] 
        
    cellfact['cellYEAR'] = [extract(row) for row in cellfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'REGION':
                return col['code'] 
        
    cellfact['REGION'] = [extract(row) for row in cellfact['Dim']]
    
    # Removing uneccessary feature columns
    cellfact.drop(['Dim', 'dataset', 'effective_date', 'end_date', 'fact_id', 'published', 'value', 'display', 'high', 'low'], axis=1, inplace=True)
    
    # Renamning data frame           
    cell = cellfact
    #cell.head()
    cell.describe()
    #cell.dtypes
    
    # Looking at null values
    null_data = cell[cell.isnull().any(axis=1)]
    #print null_data
    
    # Removing null values 
    cell = cell[cell.ISO.notnull()]
    
    # Converting year to numeric
    cell.loc[:, 'cellYEAR'] = pd.to_numeric(cell.loc[:, 'cellYEAR'])
    cell.describe()
    
    # Sorting by year and then country three letter code
    CY = cell.sort_values(['cellYEAR'],ascending=False)
    CYN = CY.drop_duplicates('ISO', keep = 'first' ).values
    
    # Create a cellphone subscription data frame, drop unecessary columns, set index to ISO 
    cell = pd.DataFrame(data=CYN)
    cell = cell.rename(columns = {0 : 'cell_Subscription%', 1 : 'ISO', 2 : 'cellYEAR', 3 : 'REGION'})
    cell.describe()
    cell.drop(['REGION'], axis=1, inplace=True) 
    
    # Converting columns to numeric 
    cell[['cell_Subscription%', 'cellYEAR']] = cell[['cell_Subscription%', 'cellYEAR']].astype(float)
    
    
    return cell