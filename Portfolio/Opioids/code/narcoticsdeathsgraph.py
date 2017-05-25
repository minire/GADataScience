
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

# US. Creating a dataframe for Maternal Mortality Rate (MMR) by US state from CSV file. Data obtained from 
#http://kff.org/
#http://hrc.nwlc.org/status-indicators/maternal-mortality-rate-100000
#https://www.guttmacher.org/state-policy/explore/overview-abortion-laws
#http://blog.estately.com/2016/03/these-are-the-most-marijuana-enthused-states-in-america/

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


# Dropping blank rows 
USMMR = USMMR[USMMR.MMR.notnull()]

# Looking at null values 
null_data = USMMR[USMMR.isnull().any(axis=1)]
print null_data

# Filling null values with the meidan for each dataset 
USMMR.fillna(USMMR.median(), inplace=True)

# Change index to state 
USMMR = USMMR.set_index(['State'])
USMMR.drop([ 'Ambulatory_Abort', 'HospNear_Abort', 'TA_Abort', 'AdmitPriv_Abort'], axis=1, inplace=True)



# Reading in the US agricultural exports for 2011
imports = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

# Change index to state 
imports = imports.set_index(['state'])
imports = imports.rename(index = {' California' : 'California'})
imports.drop([ 'beef', 'pork', 'poultry', 'dairy', 'fruits fresh', 'fruits proc', 'total fruits', 'veggies fresh', 'veggies proc', 'total veggies', 'corn', 'wheat', 'cotton', 'category'], axis=1, inplace=True)


# Reding in the Narcotic overdose statistics
narcotics = pd.read_csv('2015 narcotics deaths by state.csv')
narcotics['NormNarcDeaths'] = (narcotics['Deaths']/narcotics['Population'])*100000
narcotics.drop(['State Code', 'Crude Rate'], axis=1, inplace=True)
narcotics = narcotics.set_index(['State'])


# Weed enthusiasm by state
weed = pd.read_csv('weed.csv')
weed = weed.set_index(['State'])
weed.head()


# Adding in export information for the states 
pieces = [USMMR, imports, narcotics, weed]
opioids = pd.concat(pieces, axis=1, join_axes=[imports.index])




# Creating a list of feature columns 
features = [

]

for row in opioids:
    features.append(row)
print features


# Looking for null values
null_data = opioids[opioids.isnull().any(axis=1)]
print null_data

# In[]:



#scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
#            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]



data = [ dict(
        type='choropleth',
        #colorscale = scl,
        autocolorscale = True,
        locations = opioids['code'],
        z = opioids['NormNarcDeaths'].astype(float),
        locationmode = 'USA-states',
        text = False,
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            )
        ),
        colorbar = dict(
            title = "Narcotics Deaths per 100,000"
        )
    ) ]

layout = dict(
        title = 'Narcotics Deaths per 100,000',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)',
        ),
    )

fig = dict(data=data, layout=layout)

py.image.save_as(fig, filename='NarcoticsDeaths.png')
