
# This notebook is for exploration of WHO data with a link to WHO/GHO API resources below
#http://apps.who.int/gho/data/node.resources.api
# In[41]:
import requests
import pandas as pd 
import json
# In[42]:
# grabbing data for the adolescent birth rate 'MDG_0000000003'    
B = requests.get('http://apps.who.int/gho/athena/api/GHO/MDG_0000000003.json')

#Converting data into json format
data = B.json()
data.keys()
data['fact'][1]

#Creating a data frane that contains the adolescent birth rate (ABR) values 
facts = data['fact']
facts = pd.DataFrame(facts)
facts.keys()

# In[49]:
#STEP 1 of cleaning API: Extracting numeric values for adolescent birth rate table data.fact.values
data2 = list(facts.value)
values = pd.DataFrame(data=data2)
values.head()

# In[51]:
#STEP 2: extracting country code and year from the dimension column 
def extract(A):
    for A in foo:
        if A['category'] == 'COUNTRY':
            return A['code'] 
    
facts['COUNTRY'] = [extract(foo) for foo in facts ['Dim']]

def extract(A):
    for A in foo:
        if A['category'] == 'YEAR':
            return A['code'] 
    
facts['YEAR'] = [extract(foo) for foo in facts ['Dim']]

facts = pd.concat([facts, values], axis=1)
facts.head()
# In[53]:
#deleting unecessary feature columns, changing data frane name 
 

facts.drop(['Dim', 'comments', 'dataset', 'effective_date', 'end_date', 'published', 'value', 'display'], axis=1, inplace=True)
facts = facts.rename(columns = {'COUNTRY' : 'ISO'})
facts.head()


# In[57]:
#creating a country label dictionary  
dimension = data['dimension']
country = {
        
    }

for foo in dimension:
    for boo in foo['code']:
        ISO = None
        display = boo['display']
        for loo in boo['attr']:
            if loo['category'] == 'ISO': 
                ISO = loo['value']
        country[ISO] = display    

print country
     
       
# In[65]:
#Adding the country names to the facts dataframe  

def name(x):
    for b in country:
        if x == b:
            return country[b]

facts['COUNTRY'] = [name(a) for a in facts['ISO']]
ABR = facts
ABR.head()

ABR.drop(['high', 'low'], axis=1, inplace=True)
ABR = ABR.rename(columns = {'numeric' : 'ABR'})
ABR.head()



# In[ ]:
# grabbing data for Maternal Mortality Rate (MMR) 'MDG_0000000026' 
# Values are per 100K births     

C = requests.get('http://apps.who.int/gho/athena/api/GHO/MDG_0000000026.json')

#Converting data into json format
MMR = C.json()
MMR.keys()

# In[ ]:
MMR['fact']



#numeric values for adolescent brith rate are contained in data['fact'], making a data frame for this key in 'data'
MMR['fact'][1]
MMRfact = MMR['fact']

#creating MMR data frome from the 'fact' key 
MMRfact = pd.DataFrame(MMRfact)
MMRfact.keys()
MMRfact.head()
MMRfact.Dim[0]

#extracting values from the MMR dataframe 
MMRfact.value[0]
data3 = list(MMRfact.value)
values = pd.DataFrame(data=data3)
values.head()

#concat values onto the MMRfact data frame 
MMRfact = pd.concat([MMRfact, values], axis=1)
MMRfact.head()


#pulling the country names of of the 'Dim' key  
def extract(A):
    for A in foo:
        if A['category'] == 'COUNTRY':
            return A['code'] 
    
MMRfact['COUNTRY'] = [extract(foo) for foo in MMRfact['Dim']]

def extract(A):
    for A in foo:
        if A['category'] == 'YEAR':
            return A['code'] 
    
MMRfact['YEAR'] = [extract(foo) for foo in MMRfact['Dim']]
         
MMRfact.head()


MMRfact.drop(['Dim', 'dataset', 'effective_date', 'end_date', 'fact_id', 'published', 'value', 'display', 'high', 'low'], axis=1, inplace=True)
MMRfact = MMRfact.rename(columns = {'COUNTRY' : 'ISO'})
MMRfact.head()


# In[ ]:

MMR['dimension']

MMR['dimension'][0]

MMRdim = MMR['dimension']

#creating a country and label data frame 

country = {
        
    }

for foo in MMRdim:
    for boo in foo['code']:
        ISO = None
        display = boo['display']
        for loo in boo['attr']:
            if loo['category'] == 'ISO': 
                ISO = loo['value']
        country[ISO] = display    

print country

#concat the cntry names to the facts dataframe 
def name(x):
    for b in country:
        if x == b:
            return country[b]
            
MMRfact['COUNTRY'] = [name(a) for a in MMRfact['ISO']]
MMR = MMRfact
MMR.head()



# In[ ]:
MMR.YEAR
MMR['YEAR'] = pd.to_numeric(MMR['YEAR'])
MMR.dtypes

MMR = MMR[MMR['YEAR'] == 2015]
MMR.head()
MMR.shape


# In[ ]:
# grabbing data for births attended by a professional and antenatal coverage(at least 4 visists) 'MDG_0000000025' 
# Values are percent of births     

D = requests.get('http://apps.who.int/gho/athena/api/GHO/MDG_0000000026.json')

#Converting data into json format
Pro = D.json()
Pro.keys()

# In[ ]:
MMR['fact']



#numeric values for adolescent brith rate are contained in data['fact'], making a data frame for this key in 'data'
MMR['fact'][1]
MMRfact = MMR['fact']

#creating MMR data frome from the 'fact' key 
MMRfact = pd.DataFrame(MMRfact)
MMRfact.keys()
MMRfact.head()
MMRfact.Dim[0]

#extracting values from the MMR dataframe 
MMRfact.value[0]
data3 = list(MMRfact.value)
values = pd.DataFrame(data=data3)
values.head()

#concat values onto the MMRfact data frame 
MMRfact = pd.concat([MMRfact, values], axis=1)
MMRfact.head()


#pulling the country names of of the 'Dim' key  
def extract(A):
    for A in foo:
        if A['category'] == 'COUNTRY':
            return A['code'] 
    
MMRfact['COUNTRY'] = [extract(foo) for foo in MMRfact['Dim']]

def extract(A):
    for A in foo:
        if A['category'] == 'YEAR':
            return A['code'] 
    
MMRfact['YEAR'] = [extract(foo) for foo in MMRfact['Dim']]
         
MMRfact.head()


MMRfact.drop(['Dim', 'dataset', 'effective_date', 'end_date', 'fact_id', 'published', 'value', 'display', 'high', 'low'], axis=1, inplace=True)
MMRfact = MMRfact.rename(columns = {'COUNTRY' : 'ISO'})
MMRfact.head()


# In[ ]:

MMR['dimension']
MMR['dimension'][0]
MMRdim = MMR['dimension']

#creating a country and label data frame 
country = {
        
    }

for foo in MMRdim:
    for boo in foo['code']:
        ISO = None
        display = boo['display']
        for loo in boo['attr']:
            if loo['category'] == 'ISO': 
                ISO = loo['value']
        country[ISO] = display    

print country

#concat the cntry names to the MMR dataframe: 
def name(x):
    for b in country:
        if x == b:
            return country[b]
            
MMRfact['COUNTRY'] = [name(a) for a in MMRfact['ISO']]
MMR = MMRfact
MMR.head()


# In[ ]:

MMR.YEAR
MMR['YEAR'] = pd.to_numeric(MMR['YEAR'])
MMR.dtypes

MMR = MMR[MMR['YEAR'] == 2015]
MMR.head()
MMR.shape


# In[ ]:
null_data = ABR[ABR.isnull().any(axis=1)]
print null_data

# In[52]:
#checking rows for correct data alignment 
"""facts.iloc[30]
facts.iloc[30][0]

facts.iloc[100]
facts.iloc[100][0]

facts.iloc[188]
facts.iloc[188][0]"""
