import requests
import pandas as pd 
import json
import pickle
import numpy as np

#CDC PRAMS Socrata API documentation https://dev.socrata.com/foundry/chronicdata.cdc.gov/89yw-6p6f    
# App token documentation: https://dev.socrata.com/docs/app-tokens.html 
#CDC socrata app token: S1kvrgTpe7PHEkwnHyoo9zMau


# Grabbing data for PRAMS survey in washington state 
A = requests.get('https://chronicdata.cdc.gov/resource/ese6-rqpq.json?$$app_token=S1kvrgTpe7PHEkwnHyoo9zMau&locationabbr=WA')
   
for index, row in movies.iterrows():
    if index < 3:
        movies.loc[index, 'year'] = get_movie_year(row.title)
        sleep(1)
    else:
        break
  apptoken : S1kvrgTpe7PHEkwnHyoo9zMau
 
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
