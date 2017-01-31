
import plotly.plotly as py
import plotly.tools as tls
tls.set_credentials_file(username='minire', api_key='nkch3Fjxld6ZPE70SKpN')
import pandas as pd
import requests
import json
import pickle
import numpy as np

# US. Creating a dataframe for Maternal Mortality Rate (MMR) by US state from CSV file. Data obtained from 
#http://kff.org/
#http://hrc.nwlc.org/status-indicators/maternal-mortality-rate-100000
#https://www.guttmacher.org/state-policy/explore/overview-abortion-laws

''' Abortion scale: 
5 (unrestricted abortion to 20 weeks)
6 (very few enforced restrictions during the entire length of the pregnancy)'''

# US. Importing State MMR data from CSV
path = "../code/"
USMMR = pd.read_csv(path + 'compiled_state_data.csv')   


# Renaming coutnry column 
USMMR = USMMR.rename(columns = {'Clinic must meet structural standards comparable to ambulatory surgical centers' : 'Ambulatory_Abort'})
USMMR = USMMR.rename(columns = {'Maximum distance between clinics and hospital specified' : 'HospNear_Abort'})
USMMR = USMMR.rename(columns = {'Transfer agreement with hospital in event of complications required' : 'TA_Abort'})
USMMR = USMMR.rename(columns = {'Hospital admitting privileges or alternative agreements for clinicians required' : 'AdmitPriv_Abort'})
USMMR = USMMR.rename(columns = {'State Has Secured a Waiver or State Plan Amendment (SPA) from CMS to Cover Services' : 'Medicaid_extend_Pregnancy'})
USMMR = USMMR.rename(columns = {'births financed by medicaid (%) (2010-2015)' : 'Medicaid_Paid_births(%)'})
USMMR = USMMR.rename(columns = {'Median Annual Household Income' : 'MedianIncome($)'})
USMMR = USMMR.rename(columns = {'Contraceptives paid for by insurance' : 'Pill_InsurePol'})
USMMR = USMMR.rename(columns = {'emergency contraceptive access' : 'EC_access'})


# Mapping yes and no to numeric values 
USMMR['Ambulatory_Abort'] = USMMR['Ambulatory_Abort'].map({'Yes':1, 'No':0})
USMMR['HospNear_Abort'] = USMMR['HospNear_Abort'].map({'Yes':1, 'No':0})
USMMR['TA_Abort'] = USMMR['TA_Abort'].map({'Yes':1, 'No':0})
USMMR['AdmitPriv_Abort'] = USMMR['AdmitPriv_Abort'].map({'Yes':1, 'No':0})
USMMR['Medicaid_extend_Pregnancy'] = USMMR['Medicaid_extend_Pregnancy'].map({'Yes':1, 'No':0})
USMMR['Pill_InsurePol'] = USMMR['Pill_InsurePol'].map({'No Policy':0, 'Weak Policy':1,'Limited Policy':2, 'Meets Policy':3})
USMMR['EC_access'] = USMMR['EC_access'].map({'No Policy':0, 'Weak Policy':1,'Limited Policy':2, 'Meets Policy':3})

#Dropping blank rows 
USMMR = USMMR[USMMR.MMR.notnull()]

#looking at null values 
null_data = USMMR[USMMR.isnull().any(axis=1)]
print null_data

# Filling null values with the meidan for each dataset 
USMMR.fillna(USMMR.median(), inplace=True)

# Change index to state 
USMMR = USMMR.set_index(['State'])
#USMMR.drop(['MMR_Rank', 'prop poverty_White ', 'Prop poverty_Black', 'prop poverty_Hispanic', 'Ambulatory_Abort', 'HospNear_Abort', 'TA_Abort', 'AdmitPriv_Abort', 'TP_White 1000', 'TP_Black 1000', 'TP_Hispanic 1000', ], axis=1, inplace=True)



#reading in the US agricultural exports for 2011
imports = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

# Change index to state 
imports = imports.set_index(['state'])
imports = imports.rename(index = {' California' : 'California'})
imports.drop([ 'beef', 'pork', 'poultry', 'dairy', 'fruits fresh', 'fruits proc', 'total fruits', 'veggies fresh', 'veggies proc', 'total veggies', 'corn', 'wheat', 'cotton', 'category'], axis=1, inplace=True)

# adding in export information for the states 
pieces = [USMMR, imports]
USMMR = pd.concat(pieces, axis=1, join_axes=[imports.index])
USMMR.head()

# Creating a list of feature columns 
features = [

]

for row in USMMR:
    features.append(row)
print features

USMMR = USMMR.set_index(['code'])


# In[]: 

#py.offline.init_notebook_mode()
#help(py.offline.plot)
#from plotly.offline import plot 
#import plotly.graph_objs as go 
#help(py.graph_objs)

# In[]:



# This section defines the layout paramaters for the graph, I am not sure if this is for the whole graph or individual graphs. 
# This section also defines the dictionary that the data for each graph will be stored in 

scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

data = []
layout = dict(
    title = 'Demographics Affecting Maternal Mortality Rates<br>\
Source: <a href="">\
Multiple</a>',
    showlegend = False,
    autosize = False,
    width = 1000,
    height = 900,
    hovermode = False,
)

# This section organizes the data from the data frame into a layout structure for each graph. 
#The dictionary is highly structured to match the infor needed for a scattergeo plot. It is alos labeled with a geo_key at this time to identify the years 
#The name of the geo_key is included in this section of the code 
# the lat and longitudes here are for each individual graph (aka there are repeated lats and longs for each year)

features = ['MMR', 'MedianIncome($)', 'Medicaid_extend_Pregnancy', 'economic distress', 'Teen Birth Rate per 1,000', 'PPR_White', 'PPR non-white ', 'Abortion_Policy_rank', 'Pill_InsurePol', 'EC_access', 'State Taxes Per Capita', 'total exports']



for i in range(len(features)):
    geo_key = 'geo'+str(i+1) if i != 0 else 'geo'
    locations = list (USMMR.index)
    z = list(USMMR[features[i]].astype(float))    
    # USMMR data 
    data.append(
        dict(
            type='choropleth',
            colorscale = scl,
            autocolorscale = False,
            locations = locations,
            z = z,
            locationmode = 'USA-states',
            text = False,  
            geo = geo_key,
            name = features[i],
            marker = dict(
                line = dict (
                    color = 'rgb(255,255,255)',
                    width = 2
                    )
                )
            )
        )
  


# This section adds on labels to the small graphs in the ordered structure understood by plotly
# the lat and long here will remain the same because you want the title to be in the same spot in each graph. 
# years[i] returns the specific year that allows you to organize the data, for this I will need to build a feature dictionary to do the same thing
# the data will need to be written in using a differnt type of call statement from found in this code 


    # Year markers
    data.append(
        dict(
            type = 'scattergeo',
            showlegend = False,
            lon = [-82],
            lat = [50],
            geo = geo_key,
            text = [features[i]],
            mode = 'text',
        )
    )
      
# this section creates the dictionary that will determine the overall layout of the ensembled graphs. 
# the geo_keys are how all of the data is linked to the layout
# this layout is nested inside the main layout, the geo_key is iterated through this loop 
    
    layout[geo_key] = dict(
        scope = 'usa',
        showland = True,
        landcolor = 'rgb(229, 229, 229)',
        showcountries = False,
        domain = dict( x = [], y = [] ),
        subunitcolor = "rgb(255, 255, 255)",
    )

z = 0
COLS = 3
ROWS = 4
for y in reversed(range(ROWS)):
    for x in range(COLS):
        geo_key = 'geo'+str(z+1) if z != 0 else 'geo'
        layout[geo_key]['domain']['x'] = [float(x)/float(COLS), float(x+1)/float(COLS)]
        layout[geo_key]['domain']['y'] = [float(y)/float(ROWS), float(y+1)/float(ROWS)]
        z=z+1
        if z > 12:
            break

fig = { 'data':data, 'layout':layout }  

py.image.save_as(fig, filename='clustergraphMMR Dems.png')

# In[]

print features[0]
print geo_key
for row in data: 
    print row

print layout

# In[]
            #type = 'scattergeo',
            #showlegend=False,
            #lon = lons,
            #lat = lats,
            #geo = geo_key,
            #name = years[i],
            #marker = dict(
                #color = "rgb(0, 0, 255)",
                #opacity = 0.5)

# This section adds on labels to the small graphs in the ordered structure understood by plotly
# the lat and long here will remain the same because you want the title to be in the same spot in each graph. 
# years[i] returns the specific year that allows you to organize the data, for this I will need to build a feature dictionary to do the same thing
# the data will need to be written in using a differnt type of call statement from found in this code 


    # Year markers
    #data.append(
        #dict(
            #type = 'scattergeo',
           # showlegend = False,
          #  lon = [-78],
         #   lat = [47],
        #    geo = geo_key,
       #     text = [years[i]],
      #      mode = 'text',
     #   )
    #)



