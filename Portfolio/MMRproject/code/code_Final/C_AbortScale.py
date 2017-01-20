
import requests
import pandas as pd 
import json
import pickle
import numpy as np

# C. Creating a dataframe for Abortion policy from CSV file. Data obtained from this PDF: https://www.reproductiverights.org/sites/crr.civicactions.net/files/documents/AbortionMap_Factsheet_2013.pdf
''' scale: 
0 (abortion crimminalized, no abortions even to save the mothers life)
1 (abortion is illegal with exceptions to save the life of the motehr)
2 (to preserve health of the mother)
3 (for socioeconomic resasons or to preserve mother's health)
4 (unrestricted abortion to 14 weeks)
5 (unrestricted abortion to 20 weeks)
6 (very few enforced restrictions during the entire length of the pregnancy)'''

# Creating a function to call script from master 
def getABS():

    # C. Importing Abortion Scale CSV
    path = "../code_final/"
    ABS = pd.read_csv(path + 'abortion_scale_final.csv')   
    #print ABS.head()   
    
    # Dropping the comments and citations from the data frame  
    ABS.drop(['Comment', 'Citation'], axis=1, inplace=True)
    #ABS.head()
    
    # Importing the Country and ISO codes from WHO ABR data
    with open('CountryISO.txt', 'rb') as handle:
      country = pickle.loads(handle.read())
          
    # Normalizing the country names 
    
    def countryrenamed(x):
        for b in country:
            if x == country[b]:
                return country[b]
    
    # Adding the ISO column to the abortion scale 
    def name(x):
        for b in country:
            if x == country[b]:
                return b
                    
    ABS['ISO'] = [name(a) for a in ABS['COUNTRY']]
    
    # Renaming coutnry column 
    ABS = ABS.rename(columns = {'COUNTRY' : 'CNTRY'})
    
    # Getting rid of null ISO values 
    ABS = ABS[ABS.ISO.notnull()]
           
    return ABS

