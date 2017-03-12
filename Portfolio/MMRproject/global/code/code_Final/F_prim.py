
import requests
import pandas as pd 
import json
import pickle
import numpy as np

# Creating a function to call script from master 
def getPrim():
    
    # F. Grabbing data for Net primary school enrolment ratio (Prim) 'WHS9_87' 
    # By percent (%)
    F = requests.get('http://apps.who.int/gho/athena/api/GHO/WHS9_87.json')
    
    # Converting data into json format
    data = F.json()
    data.keys()    
    
    # Creating a data frane that contains the primary education (Prim)  
    fact = data['fact']
    Primfact = pd.DataFrame(fact)   
    Primfact.value[0]
    Primfact.Dim[0]
    
    # Extracting 'value' from the Primfact dataframe
    data6 = list(Primfact.value)
    values = pd.DataFrame(data=data6)
    values.head()
    
    # Concat values onto the Primfact data frame 
    Primfact = pd.concat([Primfact, values], axis=1)
    Primfact.head()
    
    # Pulling the country names, year, region and sex out of the Primfact['Dim'] column      
    def extract(x):
        for col in x:
            if col['category'] == 'COUNTRY':
                return col['code'] 
        
    Primfact['ISO'] = [extract(row) for row in Primfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'YEAR':
                return col['code'] 
        
    Primfact['PrimYEAR'] = [extract(row) for row in Primfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'SEX':
                return col['code'] 
        
    Primfact['SEX'] = [extract(row) for row in Primfact['Dim']]
    
    def extract(x):
        for col in x:
            if col['category'] == 'REGION':
                return col['code'] 
        
    Primfact['REGION'] = [extract(row) for row in Primfact['Dim']]
    
    # Removing uneccessary feature columns
    Primfact.drop(['Dim','comments', 'dataset', 'effective_date', 'end_date', 'fact_id', 'published', 'value', 'display', 'high', 'low'], axis=1, inplace=True)
    
     
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
    
    # Renamning data frame     
    Prim = Primfact
    #Prim.head()
    #Prim.describe()
    #Prim.dtypes
    
    # Looking for null values
    null_data = Prim[Prim.isnull().any(axis=1)]
    #print null_data
    
    # Removing null values 
    Prim = Prim[Prim.ISO.notnull()]
    
    # Changing year to a standard year format and converting year to numeric
    Prim.PrimYEAR[Prim.PrimYEAR=='2007-2012'] = 2712
    Prim['PrimYEAR'] = pd.to_numeric(Prim['PrimYEAR'])
    Prim = Prim[Prim.PrimYEAR < 2712]
    
    # Sorting by year and then country three letter code (ISO)
    # Female
    PrimFMLE = Prim[Prim['SEX'] == 'FMLE']
    PFS = PrimFMLE.sort_values(['PrimYEAR'],ascending=False)
    PFSY = PFS.drop_duplicates('ISO', keep = 'first' ).values
    # Creating a FMLE Education dataframe, drop unecessary columns, set index to ISO 
    PrimFMLEYEAR = pd.DataFrame(data=PFSY)
    PrimFMLEYEAR = PrimFMLEYEAR.rename(columns = {0 : 'ED_FMLE%', 1 : 'ISO', 2 : 'EDYEARFMLE', 3 : 'SEX', 4 : 'REGION'})
    PrimFMLEYEAR.drop(['SEX', 'REGION', 'EDYEARFMLE'], axis=1, inplace=True) 
    indexed_PrimFMLEYEAR = PrimFMLEYEAR.set_index(['ISO'])
    
    # Male 
    PrimMLE = Prim[Prim['SEX'] == 'MLE']
    PFS = PrimMLE.sort_values(['PrimYEAR'],ascending=False)
    PFSY = PFS.drop_duplicates('ISO', keep = 'first' ).values
    # Creating a MLE Education dataframe, drop unecessary columns, set index to ISO 
    PrimMLEYEAR = pd.DataFrame(data=PFSY)
    PrimMLEYEAR = PrimMLEYEAR.rename(columns = {0 : 'ED_MLE%', 1 : 'ISO', 2 : 'EDYEARMLE', 3 : 'SEX', 4 : 'REGION'})
    PrimMLEYEAR.drop(['SEX', 'REGION'], axis=1, inplace=True)
    indexed_PrimMLEYEAR = PrimMLEYEAR.set_index(['ISO'])
    
    # Concat the MLE and FMLE data frames 
    pieces = [indexed_PrimFMLEYEAR, indexed_PrimMLEYEAR]
    PrimED = pd.concat(pieces, axis=1)
    PrimED['EDFMLE_MLE%'] = PrimED['ED_FMLE%']/PrimED['ED_MLE%']*100

    # Converting select feature columns to numeric 
    PrimED[['EDFMLE_MLE%','ED_FMLE%','ED_MLE%','EDYEARMLE']] = PrimED[['EDFMLE_MLE%','ED_FMLE%','ED_MLE%','EDYEARMLE']].astype(float)

    # Resesting to numerical index 
    PrimEDreset = PrimED.reset_index()
    PrimED = PrimEDreset.rename(columns = {'index': 'ISO'})
    
    return PrimED