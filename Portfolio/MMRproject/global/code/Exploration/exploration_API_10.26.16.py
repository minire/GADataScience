
# This notebook is for exploration of WHO data with a link to WHO/GHO API resources below
#http://apps.who.int/gho/data/node.resources.api
# In[41]:
import requests
import pandas as pd 
import json
# In[42]:
# grabbing data for the adolescent birth rate 'MDG_0000000003'    
B = requests.get('http://apps.who.int/gho/athena/api/GHO/MDG_0000000003.json')
# In[43]:
#Converting data into json format
data = B.json()
data.keys()
# In[45]:
data['fact'][1]
# In[46]:
facts = data['fact']
facts = pd.DataFrame(facts)
facts.keys()
# In[47]:
facts.head()
# In[48]:
facts.value[0]
# In[49]:
#extracting numeric values from adolescent birth rate table data.fact.values
data2 = list(facts.value)
values = pd.DataFrame(data=data2)
values.head()
# In[50]:
facts.Dim[0]
# In[51]:
#extracting country code and year from the dimension column 
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
           
AdolBR = pd.concat([facts, values], axis=1)
AdolBR.head()
# In[52]:
#checking rows for alignment 
"""AdolBR.iloc[30]
AdolBR.iloc[30][0]

AdolBR.iloc[100]
AdolBR.iloc[100][0]

AdolBR.iloc[188]
AdolBR.iloc[188][0]"""
# In[53]:
#deleting unecessary feature columns, changing names and index  
AdolBR.drop(['Dim', 'comments', 'dataset', 'effective_date', 'end_date', 'published', 'value', 'display'], axis=1, inplace=True)
AdolBR = AdolBR.rename(columns = {'COUNTRY' : 'ISO'})
AdolBR.head()
# In[66]:
#indexed_AdolBR = AdolBR.set_index(['ISO'])
#indexed_AdolBR.head()
# In[55]:
#country names are contained in data['dimension'], the following cells extract the country names 
# In[56]:
#dimension data exploration
'''dimension = data['dimension']

for foo in dimension:
    if foo['label'] == "COUNTRY":
        print foo
        
dimension = data['dimension']
for foo in dimension:
    if foo['label'] == "COUNTRY":
        print foo.keys()
        
dimension = data['dimension']
for foo in dimension:
    for boo in foo['code']: 
        print boo.keys() '''
# In[57]:
#creating a country and label data frame 
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
     
# In[58]:
#cntryNames = pd.DataFrame(country.items(), columns=['ISO', 'COUNTRY'])
#cntryNames.head()
# In[67]:
#indexed_cntryNames = cntryNames.set_index(['ISO'])
#indexed_cntryNames.head()
          
# In[65]:
#concat the cntry names to the adolBR dataframe 
def name(x):
    for b in country:
        if x == b:
            return country[b]

AdolBR['COUNTRY'] = [name(a) for a in AdolBR['ISO']]
ABR = AdolBR
ABR.head()

ABR.drop(['high', 'low'], axis=1, inplace=True)
ABR = ABR.rename(columns = {'numeric' : 'ABR'})
ABR.head()

# In[ ]:
null_data = ABR[ABR.isnull().any(axis=1)]
print null_data
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
            
            
'''cntryNames = pd.DataFrame(country.items(), columns=['ISO', 'COUNTRY'])
cntryNames.head()'''


#concat the cntry names to the adolBR dataframe 
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
            
            
'''cntryNames = pd.DataFrame(country.items(), columns=['ISO', 'COUNTRY'])
cntryNames.head()'''


#concat the cntry names to the adolBR dataframe 
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

# In[33]:

#spare code for investigating API
# A.headers
# A.status_code
# A.text
#AdolBR = pd.DataFrame.from_dict(A.json(), orient = index)
#print AdolBR
#from pandas.io.json import json_normalize
#df =json_normalize(data['fact'])

#spare code for for loops: 
#for foo in facts.Dim:
#    for boo in foo:
#       if boo['category'] == 'COUNTRY':
#    country[foo[4]['category']] = foo[4]['code']
#    print country 
#facts.Dim[0][4]['category']
#facts.Dim[0][4]['code']        
#facts.Dim[0][4]


# In[ ]:



