
import requests
import pandas as pd 
import json
import pickle
import numpy as np

# Creating a function to call script from master 
def getMMR():
    
    # A. Grabbing data for Maternal mortality ratio - Mortality and global health estimates (MMR) 'MDG_0000000026' 
    # Maternal mortality ratio (per 100 000 live births)         
    A = requests.get('http://apps.who.int/gho/athena/api/GHO/MDG_0000000026.json')
    
    # Converting data into json format
    data = A.json()
    
    # Creating a data frane that contains the MMR (per 100,000 births) values 
    fact = data['fact']
    MMRfact = pd.DataFrame(fact)   
    #MMRfact.head()
    
    # Extracting values from the MMR dataframe
    data1 = list(MMRfact.value)
    values = pd.DataFrame(data=data1)
    
    # Concat values onto the MMRfact data frame 
    MMRfact = pd.concat([MMRfact, values], axis=1)
    
    # Extract the country code('COUNTRY') and year ('YEAR') from the MMRfact.Dim column
    def extract(x):
        for col in x:
            if col['category'] == 'COUNTRY':
                return col['code'] 
        
    MMRfact['COUNTRY'] = [extract(row) for row in MMRfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'YEAR':
                return col['code'] 
        
    MMRfact['MMRYEAR'] = [extract(row) for row in MMRfact['Dim']]
    
    '''def extract(x):
        for col in x:
            if col['category'] == 'REGION':
                return col['code'] 
        
    MMRfact['REGION'] = [extract(row) for row in MMRfact['Dim']]'''
       
    # Simplify dataframe, only including relevant columns, changing COUNTRY to ISO (three letter code)           
    MMRfact.drop(['Dim', 'dataset', 'effective_date', 'end_date', 'fact_id', 'published', 'value', 'display', 'high', 'low'], axis=1, inplace=True)
    MMRfact = MMRfact.rename(columns = {'COUNTRY' : 'ISO', 'numeric' : 'MMR100K'})
    
    '''# Pulling the country names out of the 'Dim' key  
    MMRdim = data['dimension']
    
    # Creating a country and ISO code dictionary 
    country = {
            
        }
    
    for row in MMRdim:
        for element in row['code']:
            ISO = None
            display = element['display']
            for x in element['attr']:
                if x['category'] == 'ISO': 
                    ISO = x['value']
            country[ISO] = display    
    
    #print country
    
    #step 5: add the country names into the MMRfact data frame
    def name(x):
        for b in country:
            if x == b:
                return country[b]
                
    MMRfact['COUNTRY'] = [name(a) for a in MMRfact['ISO']]'''
    
    # Renaming the data frame     
    MMR = MMRfact
    #MMR.dtypes
    
    # Extract data only for the year 2015 
    MMR['MMRYEAR'] = pd.to_numeric(MMR['MMRYEAR'])
    MMR = MMR[MMR['MMRYEAR'] == 2015]
    
    # Adding a column for MMR in % form
    MMR['MMR%'] = MMR['MMR100K']/1000
    
    # Creating a binary variable for MMR 
    MMR['MMRBinary'] = np.where(MMR['MMR100K'] <= 56, 1 , 0)
    
    
    # Creating a classfier variable for MMR based on quartile percents (min, 25%, 50%, 75%, Max)    
    
    def classifier(x):
        if x > 229:
            return 4 
        elif x > 56:
            return 3
        elif x > 15:
            return 2
        elif x > 3:
            return 1
        else:
            return 0
        
    MMR['MMRClassifier'] = [classifier(row) for row in MMR['MMR100K']]
    
     
    '''# compare with histogram and box plot by region
    import matplotlib.pyplot as plt
    # display plots in the notebook
    %matplotlib inline
    
    MMR.groupby('REGION').mean().drop('YEAR', axis=1).plot(kind='bar')
    MMR.boxplot(column='MMR100k', by='REGION')'''
    
    return MMR

# In[41]:

