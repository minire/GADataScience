
import requests
import pandas as pd 
import json
import pickle
import numpy as np

# Creating a function to call script from master 

def getABR():
    
    # B. Grabbing data for Adolescent birth rate 'MDG_0000000003'
    # Values per 1000 women aged 15-19 years    
    B = requests.get('http://apps.who.int/gho/athena/api/GHO/MDG_0000000003.json')
    
    # Converting data into json format
    data = B.json()
    data.keys()
    data['fact'][1]
    
    # Creating a data frame that contains the adolescent birth rate (ABR) values 
    facts = data['fact']
    facts = pd.DataFrame(facts)
    facts.keys()
    
    # Extracting numeric values for adolescent birth rate table data.fact.values
    data2 = list(facts.value)
    values = pd.DataFrame(data=data2)
    #print values.head()
        
    # Extracting country code, year and region from the dimension column 
    def extract(x):
        for col in x:
            if col['category'] == 'COUNTRY':
                return col['code'] 
        
    facts['ISO'] = [extract(row) for row in facts ['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'YEAR':
                return col['code'] 
        
    facts['YEAR'] = [extract(row) for row in facts ['Dim']]
    
    def extract(x):
       for col in x:
           if col['category'] == 'REGION':
               return col['code'] 
        
    facts['REGION'] = [extract(row) for row in facts['Dim']]      
      
    # Adding ABR values back to the facts dataframe 
    facts = pd.concat([facts, values], axis=1)
    #print facts.head()    
    
    # Deleting unecessary feature columns, changing column names     
    facts.drop(['Dim', 'comments', 'dataset', 'effective_date', 'end_date', 'published', 'value', 'display', 'fact_id', 'high', 'low'], axis=1, inplace=True)
    #print facts.head()    
      
    # Pulling the country names out of the 'Dim' key  
    factsdim = data['dimension']
    
    # Creating a country and ISO code dictionary 
    country = {
            
        }
    
    for row in factsdim:
        for element in row['code']:
            ISO = None
            display = element['display']
            for x in element['attr']:
                if x['category'] == 'ISO': 
                    ISO = x['value']
            country[ISO] = display  
    #print country
    
    # Adding the country names into the ABRfact data frame
    def name(x):
        for b in country:
            if x == b:
                return country[b]
                
    facts['COUNTRY'] = [name(a) for a in facts['ISO']]
    
    # Renaming the dataframe 
    ABR = facts
    
    # Renaming feture columns 
    ABR = ABR.rename(columns = {'numeric' : 'ABR1000', 'YEAR' : 'ABRYEAR'})
    
    # Changing ABRyear data type to float: 
    ABR[['ABRYEAR']] = ABR[['ABRYEAR']].astype(float)    
    
    # Adding a column for MMR as a percent (%)
    ABR['ABR%'] = ABR['ABR1000']/10
    
    # Removing null values 
    ABR = ABR[ABR.ISO.notnull()]
    
    return ABR