
# This notebook is for exploration of WHO data with a link to WHO/GHO API resources below
#http://apps.who.int/gho/data/node.resources.api
# In[41]:
import pandas as pd 
import numpy as np
import requests
import json
import pickle 

# In[ ]:
#creating a dataframe for maternal mortality rates by country from the WHO data set 'MDG_0000000026'
# values are per 100,000 women 
import MatMorRat
MatMorR = MatMorRat.getMMR()
indexed_MatMorR = MatMorR.set_index(['ISO'])
print indexed_MatMorR.head()


    # In[42]:
# Creating a dataframe for the adolescent birth rates by country from the WHO data set 'MDG_0000000003'
# values are per 1000 women     
import ABR
AdolBR = ABR.getABR()
indexed_AdolBR = AdolBR.set_index(['ISO'])
print indexed_AdolBR.head()


# In[ ]:

# creating a dataframe for Abortion policy from CSV file. Data obtained from this PDF: https://www.reproductiverights.org/sites/crr.civicactions.net/files/documents/AbortionMap_Factsheet_2013.pdf
# scale: 0 (abortion crimminalized, no abortions even to save the mothers life) to 6 (very few enforced restrictions during the entire length of the pregnancy)
import AbortScale
ABScale = AbortScale.getABS()
indexed_ABScale = ABScale.set_index(['ISO'])
print indexed_ABScale.head()


# In[ ]:

# Creating a data frame of life expextancy at birth in WHO countries from WHO data set 'WHOSIS_000001'
# age in years 

import AOD
LifeExpect = AOD.getAOD()
indexed_LifeExpect = LifeExpect.set_index(['ISO'])
print indexed_LifeExpect.head()

# In[ ]:
# Creating a data frame of Gross National Income (GNI) per capita based on purchasing power parity (PPP) in USD from WHO data set 'WHS9_93'
# age in years 

import GNI
GNI_PPP = GNI.getGNI()
indexed_GNI_PPP = GNI_PPP.set_index(['ISO'])
print indexed_GNI_PPP.head()


  # In[ ]:
#Concating the data frame togwther using the ISO value 
#FORMATTING IS WRONG FOR ABORTSCALE, Will have to figure out another way to add data

mother = pd.concat([indexed_MatMorR, indexed_AdolBR, indexed_LifeExpect, indexed_GNI_PPP], axis=1, join = 'inner')

# scatter matrix of feature columns 
pd.scatter_matrix(mother[['MMR%', 'ABR%', 'AOD_FMLE', 'GNI']], figsize=(10, 8))

# heat map 
import seaborn as sns 
sns.heatmap(mother[['MMR%', 'ABR%', 'AOD_FMLE', 'GNI']].corr())
# In[ ]:

# define X and y
feature_cols = ['ABR%', 'AOD_FMLE', 'GNI']
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