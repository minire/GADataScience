import requests
import pandas as pd 
import json
import pickle
import numpy as np

#import necessary API Username/Keys 
import sys 
sys.path.insert(0, '/Users/minire/dropbox/CS/keys')
import keys
print dir(keys)

#CDC PRAMS Socrata API documentation https://dev.socrata.com/foundry/chronicdata.cdc.gov/89yw-6p6f    
# App token documentation: https://dev.socrata.com/docs/app-tokens.html 



# Grabbing data for PRAMS survey in washington state 
A = requests.get('https://chronicdata.cdc.gov/resource/ese6-rqpq.json?$$app_token=keys.pramsapptoken&locationabbr=WA')

    
 
# check the status: 200 means success, 4xx means error
A.status_code
A.json()
# view the raw response text
A.text


# Converting data into json format
data = A.json()

print(dir(A))
help(A)
A.headers


print data 
# Creating a data frane 

PRAMS = pd.DataFrame(data)   
PRAMS.head()

pramsgrouped = PRAMS.groupby(by= PRAMS['locationdesc'], axis=0)
