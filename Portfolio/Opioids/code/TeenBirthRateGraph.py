
# Learn about API authentication here: https://plot.ly/pandas/getting-started
# Find your api_key here: https://plot.ly/settings/api
import sys 
sys.path.insert(0, '/Users/minire/dropbox/CS/keys')
import keys
print dir(keys)

import plotly.plotly as py
import plotly.tools as tls
tls.set_credentials_file(username=keys.pltusername, api_key=keys.pltapi_key)
import pandas as pd
import requests
import json
import pickle
import numpy as np 

#reading in the US agricultural exports for 2011
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

# Change index to state 
df = df.set_index(['state'])
df = df.rename(index = {' California' : 'California'})

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

# Mapping yes and no to numeric values 
USMMR['Ambulatory_Abort'] = USMMR['Ambulatory_Abort'].map({'Yes':1, 'No':0})
USMMR['HospNear_Abort'] = USMMR['HospNear_Abort'].map({'Yes':1, 'No':0})
USMMR['TA_Abort'] = USMMR['TA_Abort'].map({'Yes':1, 'No':0})
USMMR['AdmitPriv_Abort'] = USMMR['AdmitPriv_Abort'].map({'Yes':1, 'No':0})
USMMR['Medicaid_extend_Pregnancy'] = USMMR['Medicaid_extend_Pregnancy'].map({'Yes':1, 'No':0})

# Dropping blank rows 
USMMR = USMMR[USMMR.MMR.notnull()]

#looking at null values 
null_data = USMMR[USMMR.isnull().any(axis=1)]
print null_data

# Filling null values with the meidan for each dataset 
USMMR.fillna(USMMR.median(), inplace=True)

# Change index to state 
USMMR = USMMR.set_index(['State'])

# Creating a classfier variable for MMR based on quartile percents (min, 25%, 50%, 75%, Max)    

def classifier(x):
    if x > 14.9:
        return 4 
    elif x > 10.3:
        return 3
    elif x > 7.95:
        return 2
    elif x > 1.2:
        return 1
    else:
        return 0

USMMR['MMRClassifier'] = [classifier(row) for row in USMMR['MMR']]

pieces = [USMMR, df]
USMMR = pd.concat(pieces, axis=1, join_axes=[df.index])


scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]



data = [ dict(
        type='choropleth',
        #colorscale = scl,
        autocolorscale = False,
        locations = USMMR['code'],
        z = USMMR['Teen Birth Rate per 1,000'].astype(float),
        locationmode = 'USA-states',
        text = False,
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            )
        ),
        colorbar = dict(
            title = "Teen Birth Rate per 1,000"
        )
    ) ]

layout = dict(
        title = 'Teen Birth Rate per 1,000',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)',
        ),
    )

fig = dict(data=data, layout=layout)

py.image.save_as(fig, filename='TeenBirthRate.png')
