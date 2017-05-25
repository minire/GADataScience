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

# In[]
# Defining X and y 
feature_cols = ['MMR', 'MedianIncome($)', 'Medicaid_extend_Pregnancy', 'economic distress', 'Teen Birth Rate per 1,000', 'PPR_White', 'PPR non-white ', 'Abortion_Policy_rank', 'State Taxes Per Capita', 'total exports'] #, 'Pill_InsurePol', 'EC_access'
    
# Define X and y
X = opioids[feature_cols]
y = opioids['NormNarcDeaths']

# In[ ] :
# Importing random forest regressor for continuous variable 
from sklearn import metrics 
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor 
rfreg = RandomForestRegressor()

# In[ ]:
# Tuning n-estimators 

# List of values to try for n_estimators (the number of trees)
estimator_range = range(10, 310, 10)

# List to store the average RMSE for each value of n_estimators
RMSE_scores = []

# Use 5-fold cross-validation with each value of n_estimators (WARNING: SLOW!)
for estimator in estimator_range:
    rfreg = RandomForestRegressor(n_estimators=estimator, random_state=1)
    MSE_scores = cross_val_score(rfreg, X, y, cv=5, scoring='neg_mean_squared_error')
    RMSE_scores.append(np.mean(np.sqrt(-MSE_scores)))

# Plot n_estimators (x-axis) versus RMSE (y-axis)

import matplotlib.pyplot as plt
%matplotlib inline

plt.plot(estimator_range, RMSE_scores)
plt.xlabel('n_estimators')
plt.ylabel('RMSE (lower is better)')

# Show the best RMSE and the corresponding max_features
sorted(zip(RMSE_scores, estimator_range))[0]

# In[ ]:
# Tuning max_features
# List of values to try for max_features
feature_range = range(1, len(feature_cols)+1)

# List to store the average RMSE for each value of max_features
RMSE_scores = []

# Use 10-fold cross-validation with each value of max_features (WARNING: SLOW!)
for feature in feature_range:
    rfreg = RandomForestRegressor(n_estimators=60, max_features=feature, random_state=1)
    MSE_scores = cross_val_score(rfreg, X, y, cv=10, scoring='neg_mean_squared_error')
    RMSE_scores.append(np.mean(np.sqrt(-MSE_scores)))
    
# Plot max_features (x-axis) versus RMSE (y-axis)
plt.plot(feature_range, RMSE_scores)
plt.xlabel('max_features')
plt.ylabel('RMSE (lower is better)')  

# Show the best RMSE and the corresponding max_features
sorted(zip(RMSE_scores, feature_range))[0]

# In[ ]:
# Fitting a Random Forest with the best parameters
# Max_features=1 is best and n_estimators=40
rfreg = RandomForestRegressor(n_estimators=60, max_features=4, oob_score=True, random_state=1)
rfreg.fit(X, y)

# Compute feature importances 
features = pd.DataFrame({'feature':feature_cols, 'importance':rfreg.feature_importances_}).sort_values('importance', ascending=False)
print features
features.plot(x='feature', kind='bar')
#sum(features.importance)

# Compute the out-of-bag R-squared score
#rfreg.oob_score_
# In[]:

# Creating a new variable for optimized features 
from sklearn.feature_selection import SelectFromModel
sfm = SelectFromModel(rfreg, threshold=0.09, prefit=True)
X_important = sfm.transform(X)
print(X_important.shape[0],X_important.shape[1])

# In[ ]:
# Check the RMSE for a Random Forest that only includes important features
rfreg = RandomForestRegressor(n_estimators=60, max_features=4, random_state=1)
scores = cross_val_score(rfreg, X_important, y, cv=20, scoring='neg_mean_squared_error')
np.mean(np.sqrt(-scores))

# In[ ]:
# Check the RMSE for a Random Forest ALL features
rfreg = RandomForestRegressor(n_estimators=60, max_features=4, random_state=1)
scores = cross_val_score(rfreg, X, y, cv=20, scoring='neg_mean_squared_error')
np.mean(np.sqrt(-scores))


# In[ ]:
#print opioids['NormNarcDeaths'].mean()

# Null accuracy RMSE
def fillmean(x):
    if x != str:
        return opioids['NormNarcDeaths'].mean()
opioids['NNDmean'] = [fillmean(row) for row in opioids['NormNarcDeaths']]


from sklearn.metrics import mean_squared_error
score = mean_squared_error(opioids['NormNarcDeaths'], opioids['NNDmean'])
nullRMSE = np.mean(np.sqrt(score))
print nullRMSE 

print 1-(3.4532901044209914/4.61095354742)
# In[ ]:
    
# look at feature contributions for each response variable with a train test split 
import numpy as np 
# Train/test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)
  
from treeinterpreter import treeinterpreter as ti 
rfreg = RandomForestRegressor(n_estimators=60, max_features=4, random_state=1)
rfreg.fit(X_train, y_train)

prediction,bias, contributions = ti.predict(rfreg, X_test)

#prediction == bias + contributions 
assert(numpy.allclose(prediction, bias + np.sum(contributions, axis=1)))

sorted(zip(contributions[1], opioids.columns.values),key=lambda x: -abs(x[0]))
prediction[0]
bias[0]
contributions[0]

# In[]:
# visualizing X and y 
data_cols =['NormNarcDeaths', 'MMR', 'MedianIncome($)', 'Medicaid_extend_Pregnancy', 'economic distress', 'Teen Birth Rate per 1,000', 'PPR_White', 'PPR non-white ', 'Abortion_Policy_rank', 'Pill_InsurePol', 'EC_access', 'State Taxes Per Capita', 'total exports']
    
# scatter matrix of feature columns 
pd.scatter_matrix(opioids[data_cols], figsize=(20, 20))


# In[ ]:
#heat map 
import seaborn as sns 
sns.heatmap(opioids[data_cols].corr())

# In[]:
#Improtant feature correlations:
data_important = ['economic distress', 'MMR', 'NormNarcDeaths','Teen Birth Rate per 1,000', 'PPR non-white ', 'State Taxes Per Capita', 'total exports']
opioids[data_important].corr()
# In[]:
opioids.MMR.boxplot()    
for cols in data_important:
    print cols
    opioids['MMR'].boxplot
