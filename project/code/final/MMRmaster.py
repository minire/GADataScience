
# This notebook is for exploration of WHO data with a link to WHO/GHO API resources below
#http://apps.who.int/gho/data/node.resources.api
# In[41]:
import pandas as pd 
import numpy as np
import requests
import json
import pickle 

# In[ ]:
# A. creating a dataframe for maternal mortality rates by country from the WHO data set 'MDG_0000000026'
# values are per 100,000 women 
import MatMorRat
MatMorR = MatMorRat.getMMR()
# Removing null values 
MatMorR = MatMorR[MatMorR.ISO.notnull()] 
# reseting the index to the ISO column  
A = MatMorR.set_index(['ISO'])
A.describe()

# In[42]:
# B. Creating a dataframe for the adolescent birth rates by country from the WHO data set 'MDG_0000000003'
# values are per 1000 women     
import ABR
AdolBR = ABR.getABR()
#removing null values 
AdolBR = AdolBR[AdolBR.ISO.notnull()]
#reseting the index to the ISO column 
B = AdolBR.set_index(['ISO'])
print B.describe()

# In[ ]:
# C. creating a dataframe for Abortion policy from CSV file. Data obtained from this PDF: https://www.reproductiverights.org/sites/crr.civicactions.net/files/documents/AbortionMap_Factsheet_2013.pdf
# scale: 0 (abortion crimminalized, no abortions even to save the mothers life) to 6 (very few enforced restrictions during the entire length of the pregnancy)
import AbortScale
ABScale = AbortScale.getABS()
# checking for null values
null_data = ABScale[ABScale.isnull().any(axis=1)]
print null_data
#resetting the index to the ISO column 
C = ABScale.set_index(['ISO'])
print C.describe()

# In[ ]:
# D. Creating a data frame of life expextancy at birth in WHO countries from WHO data set 'WHOSIS_000001'
# age in years 
import AOD
LifeExpect = AOD.getAOD()
# Removing null values 
LifeExpect = LifeExpect[LifeExpect.ISO.notnull()] 
#reseting the index to the ISO column 
D = LifeExpect.set_index(['ISO'])
print D.describe()

# In[ ]:
# E. Creating a data frame of Gross National Income (GNI) per capita based on purchasing power parity (PPP) in USD from WHO data set 'WHS9_93'
# age in years 
import GNI
GNI_PPP = GNI.getGNI()
# Removing null values 
GNI_PPP = GNI_PPP[GNI_PPP.ISO.notnull()] 
#reseting the index to the ISO Column 
E = GNI_PPP.set_index(['ISO'])
print E.describe()

# In[ ]:
# F. Net primary school enrollment as a percent of total by male and female 
# shown as a percent of total 
import prim
PrimaryED = prim.getPrim()
#removing null values 
PrimaryED = PrimaryED[PrimaryED.ISO.notnull()]
#reseting the index to the ISO column 
F = PrimaryED.set_index(['ISO'])
F[['EDFMLE_MLE','ED_FMLE','ED_MLE','EDYEARMLE']] = F[['EDFMLE_MLE','ED_FMLE','ED_MLE','EDYEARMLE']].astype(float)
print F.describe()

# In[ ]:
#Concating the data frame togwther using the ISO value
#Creating a list of feature data frames 
pieces = [A, B, D, E, F]

# In[ ]:
# concating features into one dataframe with MMR 
mother = pd.concat(pieces, axis=1, join_axes=[B.index])
mother.dtypes

# In[ ]:
# creating X and y 
feature_cols = ['MMR%', 'ABR%', 'AOD_FMLE', 'GNI','Abortion_scale', 'EDFMLE_MLE']

# scatter matrix of feature columns 
pd.scatter_matrix(mother[feature_cols], figsize=(10, 8))

# heat map 
import seaborn as sns 
sns.heatmap(mother[feature_cols].corr())



mother = mother[mother.GNI.notnull()]
mother = mother[mother.AOD_MLE.notnull()]
mother = mother[mother.MMR100K.notnull()]
null_data = mother[mother.isnull().any(axis=1)]
print null_data
# In[ ]:
# Running a basic logistic regression using the MMRBinary variable
#MMRBinary if '1' MMR is lower than the global average; if '0' MMR is higher than the global average 

# define X and y
feature_cols = ['ABR%', 'AOD_FMLE', 'GNI', 'Abortion_scale']
X = mother[feature_cols]
y = mother.MMRBinary

# train/test split
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

# train a logistic regression model
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(C=1e9)
logreg.fit(X_train, y_train)

# make predictions for testing set
y_pred_class = logreg.predict(X_test)

# calculate testing accuracy
from sklearn import metrics
print metrics.accuracy_score(y_test, y_pred_class)








 # In[ ]:
#Importing the Country and ISO codes from WHO ABR data
'''with open('CountryISO.txt', 'rb') as handle:
    country = pickle.loads(handle.read())'''




# In[ ]:
#SPARE CODE 
'''null_data = ABR[ABR.isnull().any(axis=1)]
print null_data'''


#checking rows for correct data alignment 
"""facts.iloc[30]
facts.iloc[30][0]

facts.iloc[100]
facts.iloc[100][0]

facts.iloc[188]
facts.iloc[188][0]"""


'''#indexed_AODMLE = indexed_AODMLE.rename(columns = {'numeric': 'AOD_MLE'})
#indexed_AODMLE.drop(['SEX'], axis=1, inplace=True)'''

'''import numpy as np
grouped = MMR.groupby('REGION')
grouped.aggregate(np.mean)'''