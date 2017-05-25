import requests
import pandas as pd 
import numpy as np

# US. Creating a dataframe for Maternal Mortality Rate (MMR) by US state from CSV file. Data obtained from 
#http://kff.org/
#http://hrc.nwlc.org/status-indicators/maternal-mortality-rate-100000
#https://www.guttmacher.org/state-policy/explore/overview-abortion-laws

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

# Adding in export information for the states 
pieces = [USMMR, imports, narcotics]
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

# Developing a classifier variable based on the description of the Normalized Narcotics Deaths. 
opioids.describe()

def classifier(x):
    if x >= 7.88:
        return 3 
    elif x >= 5.31:
        return 2
    elif x >= 3.55:
        return 1
    else:
        return 0

opioids['NNDClassifier'] = [classifier(row) for row in opioids['NormNarcDeaths']]

opioids.NNDClassifier


# In[]
# Defining X and y 
feature_cols = ['MMR', 'MedianIncome($)', 'Medicaid_extend_Pregnancy', 'economic distress', 'Teen Birth Rate per 1,000', 'PPR_White', 'PPR non-white ', 'Abortion_Policy_rank', 'State Taxes Per Capita', 'total exports'] #, 'Pill_InsurePol', 'EC_access'
    
# Define X and y
X = opioids[feature_cols]
y = opioids['NNDClassifier']

# In[]:
# Train/test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)

# Train a logistic regression model
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(C=1e9)
logreg.fit(X_train, y_train)

# Make predictions for testing set
y_pred_class = logreg.predict(X_test)

# Calculate testing accuracy
from sklearn import metrics
print metrics.accuracy_score(y_test, y_pred_class)

# In[]:

from sklearn.cross_validation import cross_val_score
scores = cross_val_score(logreg, X, y, cv=10, scoring='accuracy')
print np.mean(scores)   
    
    
    
    
    
    
    