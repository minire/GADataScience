
import requests
import pandas as pd 
import json
import pickle
import numpy as np

# US. Creating a dataframe for Maternal Mortality Rate (MMR) by US state from CSV file. Data obtained from 
#http://kff.org/
#http://hrc.nwlc.org/status-indicators/maternal-mortality-rate-100000
#https://www.guttmacher.org/state-policy/explore/overview-abortion-laws

# US. Importing State MMR data from CSV
path = "../USstate/"
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
USMMR.drop([ 'Ambulatory_Abort', 'HospNear_Abort', 'TA_Abort', 'AdmitPriv_Abort'], axis=1, inplace=True)



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

#USMMR.describe()
#USMMR.head()
#USMMR.dtypes

# In[ ]:

# Defining X and y 
feature_cols = [ 'MedianIncome($)', 'Medicaid_extend_Pregnancy', 'economic distress', 'obesity in women (%)', 'Medicaid_Paid_births(%)', 'Teen Birth Rate per 1,000', 'PPR_White', 'PPR non-white ', 'Abortion_Policy_rank', 'Pill_InsurePol', 'EC_access', 'State Taxes Per Capita', 'total exports']

# define X and y
X = USMMR[feature_cols]
y = USMMR['MMR']

# In[ ] :
# importing random forest regressor for continuous variable 
from sklearn import metrics 
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestRegressor 
rfreg = RandomForestRegressor()

# In[ ]:
# tuning n-estimators 

# list of values to try for n_estimators (the number of trees)
estimator_range = range(10, 310, 10)

# list to store the average RMSE for each value of n_estimators
RMSE_scores = []

# use 5-fold cross-validation with each value of n_estimators (WARNING: SLOW!)
for estimator in estimator_range:
    rfreg = RandomForestRegressor(n_estimators=estimator, random_state=1)
    MSE_scores = cross_val_score(rfreg, X, y, cv=5, scoring='mean_squared_error')
    RMSE_scores.append(np.mean(np.sqrt(-MSE_scores)))

# plot n_estimators (x-axis) versus RMSE (y-axis)

import matplotlib.pyplot as plt
%matplotlib inline

plt.plot(estimator_range, RMSE_scores)
plt.xlabel('n_estimators')
plt.ylabel('RMSE (lower is better)')

# show the best RMSE and the corresponding max_features
sorted(zip(RMSE_scores, estimator_range))[0]

# In[ ]:
# Tuning max_features
# list of values to try for max_features
feature_range = range(1, len(feature_cols)+1)

# list to store the average RMSE for each value of max_features
RMSE_scores = []

# use 10-fold cross-validation with each value of max_features (WARNING: SLOW!)
for feature in feature_range:
    rfreg = RandomForestRegressor(n_estimators=130, max_features=feature, random_state=1)
    MSE_scores = cross_val_score(rfreg, X, y, cv=10, scoring='mean_squared_error')
    RMSE_scores.append(np.mean(np.sqrt(-MSE_scores)))
    
# plot max_features (x-axis) versus RMSE (y-axis)
plt.plot(feature_range, RMSE_scores)
plt.xlabel('max_features')
plt.ylabel('RMSE (lower is better)')  

# show the best RMSE and the corresponding max_features
sorted(zip(RMSE_scores, feature_range))[0]

# In[ ]:
# Fitting a Random Forest with the best parameters
# Max_features=1 is best and n_estimators=40
rfreg = RandomForestRegressor(n_estimators=130, max_features=4, oob_score=True, random_state=1)
rfreg.fit(X, y)

#compute feature importances 
pd.DataFrame({'feature':feature_cols, 'importance':rfreg.feature_importances_}).sort_values('importance', ascending=False)

# compute the out-of-bag R-squared score
#rfreg.oob_score_
# In[]:

# Creating a new variable for optimized features 
from sklearn.feature_selection import SelectFromModel
sfm = SelectFromModel(rfreg, threshold=0.1, prefit=True)
X_important = sfm.transform(X)
print(X_important.shape[0],X_important.shape[1])

# In[ ]:
# Check the RMSE for a Random Forest that only includes important features
rfreg = RandomForestRegressor(n_estimators=130, max_features=4, random_state=1)
scores = cross_val_score(rfreg, X_important, y, cv=10, scoring='mean_squared_error')
np.mean(np.sqrt(-scores))

# In[ ]:
# Check the RMSE for a Random Forest ALL features
rfreg = RandomForestRegressor(n_estimators=130, max_features=4, random_state=1)
scores = cross_val_score(rfreg, X, y, cv=20, scoring='mean_squared_error')
np.mean(np.sqrt(-scores))


# In[ ]:

# Null accuracy RMSE
def fillmean(x):
    if x != str:
        return USMMR['MMR'].mean()
USMMR['MMRmean'] = [fillmean(row) for row in USMMR['MMR']]


from sklearn.metrics import mean_squared_error
score = mean_squared_error(USMMR['MMR'], USMMR['MMRmean'])
nullRMSE = np.mean(np.sqrt(score))
print nullRMSE 

# In[ ]:

# visualizing X and y 
data_cols =['Medicaid_extend_Pregnancy', 'economic distress', 'Teen Birth Rate per 1,000', 'Abortion_Policy_rank', 'Pill_InsurePol', 'EC_access', 'State Taxes Per Capita', 'total exports'] #'obesity in women (%)', 'Medicaid_Paid_births(%)','MedianIncome($)'

# scatter matrix of feature columns 
pd.scatter_matrix(USMMR[data_cols], figsize=(20, 20))


# In[ ]:
#heat map 
import seaborn as sns 
sns.heatmap(USMMR[data_cols].corr())

# In[]:
# Investigating and Optimizing features based on Feature Importance 
from sklearn.feature_selection import SelectFromModel
sfm = SelectFromModel(rfreg,threshold=0.1, prefit=True)
print(sfm.transform(X).shape[0],sfm.transform(X).shape[1])

sfm = SelectFromModel(rfreg, threshold='mean', prefit=True)
print(sfm.transform(X).shape[0],sfm.transform(X).shape[1])

sfm = SelectFromModel(rfreg, threshold='median', prefit=True)
print(sfm.transform(X).shape[0],sfm.transform(X).shape[1])

# In[ ]:

# Creating a new variable for optimized features 
sfm = SelectFromModel(rfreg, threshold='median', prefit=True)
X_important = sfm.transform(X)
print(X_important.shape[0],X_important.shape[1])

# In[ ]:

'''# Creating a classfier variable for MMR based on quartile percents (min, 25%, 50%, 75%, Max)    

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
    
USMMR['MMRClassifier'] = [classifier(row) for row in USMMR['MMR']]'''
