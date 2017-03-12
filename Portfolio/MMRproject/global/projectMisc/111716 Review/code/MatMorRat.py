# In[41]:
import requests
import pandas as pd 
import json
import numpy as np


# Creating a function to call script from master 
def getMMR():
    
    # grabbing data for Maternal Mortality Rate (MMR) 'MDG_0000000026' 
    # Values are per 100K births         
    C = requests.get('http://apps.who.int/gho/athena/api/GHO/MDG_0000000026.json')
    
    #Converting data into json format
    data = C.json()
    
    #Step1: Creating a data frane that contains the MMR (per 100,000 births) values 
    fact = data['fact']
    MMRfact = pd.DataFrame(fact)   
    #MMRfact.head()
    
    #Step2: extracting values from the MMR dataframe
    data3 = list(MMRfact.value)
    values = pd.DataFrame(data=data3)
    
    #concat values onto the MMRfact data frame 
    MMRfact = pd.concat([MMRfact, values], axis=1)
    
    #Step 3: extract the country code('COUNTRY') and year ('YEAR') from the MMRfact.Dim column
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
    
    def extract(x):
        for col in x:
            if col['category'] == 'REGION':
                return col['code'] 
        
    MMRfact['REGION'] = [extract(row) for row in MMRfact['Dim']]
       
    # simplify dataframe, only including relevant columns, changing COUNTRY to ISO (three letter code)           
    MMRfact.drop(['Dim', 'dataset', 'effective_date', 'end_date', 'fact_id', 'published', 'value', 'display', 'high', 'low'], axis=1, inplace=True)
    MMRfact = MMRfact.rename(columns = {'COUNTRY' : 'ISO', 'numeric' : 'MMR100K'})
    
     
    #Step 4 pulling the country names out of the 'Dim' key  
    MMRdim = data['dimension']
    
    #creating a country and ISO code dictionary 
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
                
    MMRfact['COUNTRY'] = [name(a) for a in MMRfact['ISO']]
    MMR = MMRfact
    
    
    #step 6: extract data only for the year 2015 
    MMR['MMRYEAR'] = pd.to_numeric(MMR['MMRYEAR'])
    #MMR.dtypes
    
    MMR = MMR[MMR['MMRYEAR'] == 2015]
    
    # adding a column for MMR in decimal form
    MMR['MMR%'] = MMR['MMR100K']/100000
    
    # creating a binary variable for MMR 
    MMR['MMRBinary'] = np.where(MMR.MMR100K <= 56, 1 , 0)
    MMR.head()
    
    '''# compare with histogram and box plot by region
    import matplotlib.pyplot as plt
    # display plots in the notebook
    %matplotlib inline
    
    MMR.groupby('REGION').mean().drop('YEAR', axis=1).plot(kind='bar')
    MMR.boxplot(column='MMR100k', by='REGION')'''
    
    return MMR

# In[41]:

