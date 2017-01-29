
# In[41]:
import requests
import pandas as pd 
import json

# In[42]:
# Creating a function to call script from master 

def getABR():
    
    # grabbing data for the adolescent birth rate 'MDG_0000000003'
    # values are per 1000 women     
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
    #print values.head()
    
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
    
    
    # In[41]: STEP 3: Adding ABR values back to the facts dataframe 
    
    facts = pd.concat([facts, values], axis=1)
    #print facts.head()
    
    # In[53]:
    #STEP 4: Deleting unecessary feature columns, changing column names
     
    facts.drop(['Dim', 'comments', 'dataset', 'effective_date', 'end_date', 'published', 'value', 'display', 'fact_id', 'high', 'low'], axis=1, inplace=True)
    facts = facts.rename(columns = {'COUNTRY' : 'ISO'})
    #print facts.head()
    
    
    # In[57]:
    '''#STEP 5: Creating a country label dictionary from the data.dimension key 
    
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
    
    # creating a txt file with the Country ISO dictionary 
    import pickle
    with open('CountryISO.txt', 'wb') as handle:
        pickle.dump(country, handle)
        
    #print country        
    
    #STEP 6: Adding the country names from the dictionary in STEP 5 to the facts dataframe from STEP 4  
    
    def name(x):
        for b in country:
            if x == b:
                return country[b]
    
    facts['COUNTRY'] = [name(a) for a in facts['ISO']]'''
    
    # In[ ]:
    #renaming The dataframe 
    ABR = facts
    
    
    #ABR.drop(['high', 'low'], axis=1, inplace=True)
    ABR = ABR.rename(columns = {'numeric' : 'ABR1000', 'YEAR' : 'ABRYEAR'})
    
    # adding a column for MMR in decimal form
    ABR['ABR%'] = ABR['ABR1000']/1000
    
    # Removing null values 
    ABR = ABR[ABR.ISO.notnull()]
    ABR
    # In[41]: loading dataframe into master  
    
    return ABR