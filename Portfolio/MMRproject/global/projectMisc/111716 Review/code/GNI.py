# In[41]:
import requests
import pandas as pd 
import json
import pickle
import numpy as np

# Creating a function to call script from master 
def getGNI():
    
    # grabbing data for Maternal Mortality Rate (MMR) 'MDG_0000000026' 
    # Values are per 100K births         
    D = requests.get('http://apps.who.int/gho/athena/api/GHO/WHS9_93.json')
    
    #Converting data into json format
    data = D.json()
    data.keys()
    
    #Creating a data frane that contains the GNI per capita PPP (purchasing power) by country:  
    fact = data['fact']
    GNIfact = pd.DataFrame(fact)   
    
    #extracting the 'values' column from the GNIfact dataframe
    data4 = list(GNIfact.value)
    values = pd.DataFrame(data=data4)
    
    
    #concat values onto the MMRfact data frame 
    GNIfact = pd.concat([GNIfact, values], axis=1)
    
    #pulling the country ISO Codes and year out of the 'Dim' key and loading into anew column in the dataframe
        
    def extract(x):
        for col in x:
            if col['category'] == 'COUNTRY':
                return col['code']
        
    GNIfact['COUNTRY'] = [extract(row) for row in GNIfact['Dim']]
    
    
    def extract(x):
        for col in x:
            if col['category'] == 'YEAR':
                return col['code'] 
        
    GNIfact['GNIYEAR'] = [extract(row) for row in GNIfact['Dim']]
    
    
    
    GNIfact.drop(['Dim', 'dataset', 'effective_date', 'end_date', 'published', 'value', 'display', 'high', 'low', 'comments', 'fact_id'], axis=1, inplace=True)
    GNIfact = GNIfact.rename(columns = {'COUNTRY' : 'ISO', 'numeric' : 'GNI'})
    
     
    '''#pulling the country names of of the 'Dim' key  
    GNIdim = data['dimension']
    
    #creating a country and label data frame 
    country = {
            
        }
    
    for row in GNIdim:
        for element in row['code']:
            ISO = None
            display = element['display']
            for x in element['attr']:
                if x['category'] == 'ISO': 
                    ISO = x['value']
            country[ISO] = display    
    
    #print country
    
    #concat the cntry names to the facts dataframe 
    def name(x):
        for b in country:
            if x == b:
                return country[b]
                
    GNIfact['COUNTRY'] = [name(a) for a in GNIfact['ISO']]'''
    
    #renaming the data frame 
    GNI = GNIfact
    
    #checking for null values 
    null_data = GNI[GNI.isnull().any(axis=1)]
    #print null_data
    
    # removing rows that don't have an ISO value 
    GNI = GNI[GNI.ISO.notnull()]
    
    #converting YEAR into a numeric data type and looking for the most recent and complete data set, went with 2012  
    GNI['GNIYEAR'] = pd.to_numeric(GNI['GNIYEAR'])
    GNI2012 = GNI[GNI['GNIYEAR'] == 2012]
    
    
    #grouped = GNI2012.groupby('ISO')
    #grouped.aggregate(np.mean)
    
    return GNI2012