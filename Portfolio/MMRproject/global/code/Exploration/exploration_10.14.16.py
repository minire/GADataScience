'''
CLASS: Getting Maternal Mortality rates form WHO- GHO


'''

# Link to the global health observatory API description page
#http://apps.who.int/gho/data/node.resources.api

# Look through the API description links and examples to see what use you have avaialble



# Use the requests library to interact with a URL

import requests
import pandas as pd 
import json
# Use a URL example in a browser to see the result returned and the use request to access with python
# http://apps.who.int/gho/athena/api/

    
A = requests.get('http://apps.who.int/gho/athena/api/GHO/MDG_0000000003.json?')
A = [json.loads(row) for row in A]

A.status_code
A.headers
resp_json = A.json()
A.json()

Adol_BR = pd.DataFrame.from_dict(A.json(), sep=' ', orient = "index")



Adol_BR[0].dimension

M = requests.get('http://apps.who.int/gho/athena/api/GHO/MDG_0000000026?format=json')
M.keys()
M.headers
M.text
resp_json = M.json()

print M.json()

url = ''

codes = pd.read_table(url)
codes.head()
print codes

# extract the maternal motality rate by country 
r = requests.get('http://apps.who.int/gho/athena/api/GHO/mdg_')
r.json()


# Hint the syntax for more than one language number is similar to one we use for multiple elements in a list


# check the status: 200 means success, 4xx means error
r.status_code


# view the raw response text
r.text

# Convert to json()

r.json()
# 
#look at the contents of the output of the json() method.  It looks like it can easily become a list of lists

# Convert the jason() method output into a dataframe with the first list as the column header and the rest as rows of data
import pandas as pd
df = pd.DataFrame.from_dict(r.json())
df.columns = df.iloc[0]
df = df[1:]




# Sort the dataframe decending by the number of people speaking the language
# Check the data type of 'EST', the number of people that speak the language

df['EST'] = pd.to_numeric(df['EST'])
df.sort_values(by='EST', ascending = [False])


# Now create a new request that brings in the stats for all the us and primary languages
# See the websites links for syntax for us and range of language nunbers



### Bonus
# Create a loop that will collect the counts of Spanish language speakers by state
