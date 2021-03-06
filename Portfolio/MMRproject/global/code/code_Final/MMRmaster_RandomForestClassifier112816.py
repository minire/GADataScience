# This master script imports data sets from python scripts A-K and creates a final maternal motality rate data frame with feature columns 
# A description of the WHO API can be found here: http://apps.who.int/gho/data/node.resources.api

import pandas as pd 
import numpy as np
import requests
import json
import pickle 

# In[ ]:
# A. Grabbing data for Maternal mortality ratio - Mortality and global health estimates (MMR) 'MDG_0000000026' 
# Maternal mortality ratio (per 100 000 live births)       

import A_MatMorRat
MatMorR = A_MatMorRat.getMMR()
# Removing null values 
MatMorR = MatMorR[MatMorR.ISO.notnull()] 
# Reseting the index to the ISO column  
A = MatMorR.set_index(['ISO'])
A.describe()

# In[42]:
# B. Grabbing data for Adolescent birth rate 'MDG_0000000003'
# Values per 1000 women aged 15-19 years 

import B_ABR
AdolBR = B_ABR.getABR()
# Removing null values 
AdolBR = AdolBR[AdolBR.ISO.notnull()]
# Reseting the index to the ISO column 
B = AdolBR.set_index(['ISO'])
print B.describe()

# In[ ]:
# C. Creating a dataframe for Abortion policy from CSV file. Data obtained from this PDF: https://www.reproductiverights.org/sites/crr.civicactions.net/files/documents/AbortionMap_Factsheet_2013.pdf
''' scale: 
0 (abortion crimminalized, no abortions even to save the mothers life)
1 (abortion is illegal with exceptions to save the life of the motehr)
2 (to preserve health of the mother)
3 (for socioeconomic resasons or to preserve mother's health)
4 (unrestricted abortion to 14 weeks)
5 (unrestricted abortion to 20 weeks)
6 (very few enforced restrictions during the entire length of the pregnancy)'''

import C_AbortScale
ABScale = C_AbortScale.getABS()

# Checking for null values
null_data = ABScale[ABScale.isnull().any(axis=1)]
print null_data

# Resetting the index to the ISO column 
C = ABScale.set_index(['ISO'])
C.drop(['CNTRY'], axis=1, inplace=True)
print C.describe()

# In[ ]:
# D. Grabbing data for Life expectancy at birth (or age of death AOD) "WHOSIS_000001"
# Life expectancy in years 

import D_LifeExpect
LifeExpect = D_LifeExpect.getAOD()
# Removing null values 
LifeExpect = LifeExpect[LifeExpect.ISO.notnull()] 
# Reseting the index to the ISO column 
D = LifeExpect.set_index(['ISO'])
print D.describe()

# In[ ]:
# E. Grabbing data for Gross national income per capita (GNI) 'WHS9_93' 
# Values are per capita purchasing power parity (PPP) int. $ 

import E_GNI
GNI_PPP = E_GNI.getGNI()
# Removing null values 
GNI_PPP = GNI_PPP[GNI_PPP.ISO.notnull()] 
# Reseting the index to the ISO Column 
E = GNI_PPP.set_index(['ISO'])
print E.describe()

# In[ ]:
# F. Grabbing data for Net primary school enrolment ratio (Prim) 'WHS9_87' 
# By percent (%)

import F_prim
PrimaryED = F_prim.getPrim()
# Removing null values 
PrimaryED = PrimaryED[PrimaryED.ISO.notnull()]
# Reseting the index to the ISO column 
F = PrimaryED.set_index(['ISO'])
#F[['EDFMLE_MLE','ED_FMLE','ED_MLE','EDYEARMLE']] = F[['EDFMLE_MLE','ED_FMLE','ED_MLE','EDYEARMLE']].astype(float)
print F.describe()
# In[ ]:
# G. Grabbing data for cellular subscribers (per 100 population) 'WHS9_CS'
# Data given as a percent (%)

import G_cell
cellphones = G_cell.getCell()
# Removing null values 
cellphones = cellphones[cellphones.ISO.notnull()]
# Reseting the index to the ISO column 
G = cellphones.set_index(['ISO'])

print G.describe()
# In[ ]:
# H. grabbing data for contraceptive prevalence - modern methods (%) 'cpmo' 
# Data in percent (%)

import H_cpmo
contraceptives = H_cpmo.getcontra()
# Removing null values 
contraceptives = contraceptives[contraceptives.ISO.notnull()]
# Reseting the index to the ISO column 
H = contraceptives.set_index(['ISO'])

print H.describe()

# In[ ]:
# I. Grabbing data for births attended by skilled health personnel (%) 'MDG_0000000025'
# Data in percent (%)

import I_attend
attend = I_attend.getattend()
# Removing null values 
attend = attend[attend.ISO.notnull()]
# Reseting the index to the ISO column 
I = attend.set_index(['ISO'])

print I.describe()
# In[ ]:
# J. grabbing data for antenatal care coverage - at least four visits (%) 'whs4_154': 
# Data as a percent (%)  

import J_prenatal
prenatal = J_prenatal.getPrenat()
# Removing null values 
prenatal = prenatal[prenatal.ISO.notnull()]
# Reseting the index to the ISO column 
J = prenatal.set_index(['ISO'])

print J.describe()

# In[ ]:
# K. Grabbing data for estimates of rates of homicide 'VIOLENCE_HOMICIDERATE'
# Per 100 000 population   

import K_homicide
homicide = K_homicide.gethomicide()
# Removing null values 
homicide = homicide[homicide.ISO.notnull()]
# Reseting the index to the ISO column 
K = homicide.set_index(['ISO'])

print K.describe()

# In[ ]:
# Concating the data frame togwther using the ISO value
# Creating a list of feature data frames 
pieces = [A, B, C, D, E, F, G, H, I, J, K]

# Concating features into one dataframe with MMR 
mother = pd.concat(pieces, axis=1, join_axes=[C.index])

 # In[ ]: 
# Filling missing values for contraceptive usage 

# Creating a contraceptive median feature 
def classifier(x):
    if x == 'AFR':
        return 23.36 
    elif x == 'AMR':
        return 49.96
    elif x == 'EMR':
        return 29.51
    elif x == 'EUR':
        return 29.54
    elif x == 'SEAR':
        return 49.63
    elif x == 'WPR':
        return 47.45
    else:
        return 0

mother['contraRegMed'] = [classifier(row) for row in mother['REGION']]

# Creating multiple contraceptive features to try in model
mother['contraRegFill'] = mother['contraceptives%']
# Filling missing contraceptive values with median values from WHO world region 
mother['contraRegFill'].fillna(mother.contraRegMed, inplace=True)
# Filling missing contraceptive values with global median value 
mother['contraceptives%'].fillna(mother['contraceptives%'].median(), inplace=True)

mother.dtypes

 # In[ ]:

# Filling remaining missing values 
mother.fillna(mother.median(), inplace=True)

# Checking for missing values 
null_data = mother[mother.isnull().any(axis=1)]
print null_data
    
# In[ ]:

# Running a basic logistic regression using the MMRBinary variable
feature_cols = ['AOD_FMLE', 'attend%', 'GNI', 'ABR%', 'EDFMLE_MLE%', 'cell_Subscription%', 'homicide100K', 'contraceptives%', 'prenat%', 'ED_FMLE%' , 'Abortion_scale'] # 'contraRegMed', 'contraRegFill', 

# Define X and y
X = mother[feature_cols]
y = mother['MMRClassifier']

# In[ ] :
# Importing random forest regressor for continuous variable 
from sklearn import metrics 
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import RandomForestClassifier
rfreg = RandomForestClassifier()
rfreg

import numpy as np
# In[ ]:
# Tuning n-estimators 
# List of values to try for n_estimators (the number of trees)
estimator_range = range(10, 500, 20)

# List to store the average RMSE for each value of n_estimators
ACU_scores = []

# Use 5-fold cross-validation with each value of n_estimators
for estimator in estimator_range:
    rfreg = RandomForestClassifier(n_estimators=estimator, random_state=1)
    scores = cross_val_score(rfreg, X, y, cv=10, scoring='accuracy')
    ACU_scores.append(np.mean(scores))
# In[ ]
# Plot n_estimators (x-axis) versus RMSE (y-axis)
%matplotlib inline
import matplotlib.pyplot as plt

plt.plot(estimator_range, ACU_scores)
plt.xlabel('n_estimators')
plt.ylabel('ACU')

# Show the best RMSE and the corresponding max_features
sorted(zip(ACU_scores, estimator_range),reverse=True)[0]

# In[ ]:
# Tuning max_features
# List of values to try for max_features
feature_range = range(1, len(feature_cols)+1)

# List to store the average RMSE for each value of max_features
ACU_scores = []

# Use 10-fold cross-validation with each value of max_features
for feature in feature_range:
    rfreg = RandomForestClassifier(n_estimators=490, max_features=feature, random_state=1)
    scores = cross_val_score(rfreg, X, y, cv=10, scoring='accuracy')
    ACU_scores.append(np.mean(scores))
    
# Plot max_features (x-axis) versus RMSE (y-axis)
plt.plot(feature_range, ACU_scores)
plt.xlabel('max_features')
plt.ylabel('ACU')  

# Show the best RMSE and the corresponding max_features
sorted(zip(ACU_scores, feature_range), reverse=True)[0]

# In[ ]:
# Fitting a Random Forest with the best parameters
# Max_features=1 is best and n_estimators=40
rfreg = RandomForestClassifier(n_estimators=490, max_features=5, oob_score=True, random_state=1)
rfreg.fit(X, y)

# Compute feature importances 
pd.DataFrame({'feature':feature_cols, 'importance':rfreg.feature_importances_}).sort_values('importance', ascending=False)

# In[ ]:
# Compute the out-of-bag R-squared score
rfreg.oob_score_

# In[ ]:
# Optimizing features 
from sklearn.feature_selection import SelectFromModel
sfm = SelectFromModel(rfreg,threshold=0.1, prefit=True)
print(sfm.transform(X).shape[0],sfm.transform(X).shape[1])

sfm = SelectFromModel(rfreg, threshold='mean', prefit=True)
print(sfm.transform(X).shape[0],sfm.transform(X).shape[1])

sfm = SelectFromModel(rfreg, threshold='median', prefit=True)
print(sfm.transform(X).shape[0],sfm.transform(X).shape[1])

# In[ ]:

sfm = SelectFromModel(rfreg, threshold=0.1, prefit=True)
X_important = sfm.transform(X)
print(X_important.shape[0],X_important.shape[1])

# In[ ]:
# Check the Accuracy Score for a Random Forest that only includes important features
rfreg = RandomForestClassifier(n_estimators=490, max_features=1, random_state=1)
scores = cross_val_score(rfreg, X_important, y, cv=10, scoring='accuracy')
np.mean(scores)

# In[ ]:
# check the Accuracy Score for a Random Forest that only includes ALL features
rfreg = RandomForestClassifier(n_estimators=330, max_features=2, random_state=1)
scores = cross_val_score(rfreg, X, y, cv=10, scoring='accuracy')
np.mean(scores)


