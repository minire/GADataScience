# In[41]:
import requests
import pandas as pd 
import json
import pickle
import numpy as np

# Creating a function to call script from master 
def getAOD():
    
    # grabbing data for life expectancy in years (or age of death AOD) 
    E = requests.get('http://apps.who.int/gho/athena/api/GHO/WHOSIS_000001.json')
    
    #Converting data into json format
    data = E.json()
    data.keys()
    
    
    #Creating a data frane that contains the adolescent birth rate (ABR) values 
    fact = data['fact']
    AODfact = pd.DataFrame(fact)   
    AODfact.value[0]
    AODfact.Dim[0]
    
    #extracting 'value' from the AODfact dataframe
    data5 = list(AODfact.value)
    values = pd.DataFrame(data=data5)
    
    #concat values onto the AODfact data frame 
    AODfact = pd.concat([AODfact, values], axis=1)
    AODfact.head()
    
    #pulling the country names, year, and sex out of the AODfact['Dim'] column  
    
    def extract(x):
        for col in x:
            if col['category'] == 'COUNTRY':
                return col['code'] 
        
    AODfact['COUNTRY'] = [extract(row) for row in AODfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'YEAR':
                return col['code'] 
        
    AODfact['AODYEAR'] = [extract(row) for row in AODfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'SEX':
                return col['code'] 
        
    AODfact['SEX'] = [extract(row) for row in AODfact['Dim']]
    
    
    AODfact.drop(['Dim', 'dataset', 'effective_date', 'end_date', 'fact_id', 'published', 'value', 'display', 'high', 'low'], axis=1, inplace=True)
    AODfact = AODfact.rename(columns = {'COUNTRY' : 'ISO'})
    
     
    '''#pulling the country names of of the 'Dim' key  
    AODdim = data['dimension']
    
    #creating a country and label dictionary
    
    country = {
            
        }
    
    for row in AODdim:
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
                
    AODfact['COUNTRY'] = [name(a) for a in AODfact['ISO']]'''
    
    
    #renamning data frame     
    AOD = AODfact
    #AOD.head()
    
    # Removing null values 
    AOD = AOD[AOD.ISO.notnull()]
    
    #and extracting life expectancy values from only 2015
    AOD['AODYEAR'] = pd.to_numeric(AOD['AODYEAR'])
    AOD= AOD[AOD['AODYEAR'] == 2015]
    
    
    # Add extra rows to the AOD data frame for MLE, FMLE and BTSX
    #separating the SEX column into three different data frames
    AODMLE = AOD[AOD['SEX'] == 'MLE']
    AODFMLE = AOD[AOD['SEX'] == 'FMLE']
    AODBTSX = AOD[AOD['SEX'] == 'BTSX']
    
    
    # reindexing the dataframes on ISO value 
    indexed_AODMLE = AODMLE.set_index(['ISO'])
    indexed_AODMLE = indexed_AODMLE.rename(columns = {'numeric': 'AOD_MLE'})
    indexed_AODMLE.drop(['SEX'], axis=1, inplace=True)
    
    indexed_AODFMLE = AODFMLE.set_index(['ISO'])
    indexed_AODFMLE = indexed_AODFMLE.rename(columns = {'numeric': 'AOD_FMLE'})
    indexed_AODFMLE.drop(['SEX', 'AODYEAR'], axis=1, inplace=True)
    
    indexed_AODBTSX = AODBTSX.set_index(['ISO'])
    indexed_AODBTSX = indexed_AODBTSX.rename(columns = {'numeric': 'AOD_BTSX'})
    indexed_AODBTSX.drop(['SEX', 'AODYEAR'], axis=1, inplace=True)
    
    
    # conactenating AOD for MLE, FMLE, and BTSX 
    AOD2015 = pd.concat([indexed_AODMLE, indexed_AODFMLE, indexed_AODBTSX], axis=1)
    
    #resesting to numerical index 
    AODreset = AOD2015.reset_index()
    AODfinal = AODreset.rename(columns = {'index': 'ISO'})
          
    return AODfinal