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
# reseting the index to the ISO column  
A = MatMorR.set_index(['ISO'])
A.describe()

# In[42]:
# B. Grabbing data for Adolescent birth rate 'MDG_0000000003'
# Values per 1000 women aged 15-19 years 

import B_ABR
AdolBR = B_ABR.getABR()
#removing null values 
AdolBR = AdolBR[AdolBR.ISO.notnull()]
#reseting the index to the ISO column 
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

# checking for null values
null_data = ABScale[ABScale.isnull().any(axis=1)]
print null_data

#resetting the index to the ISO column 
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
#reseting the index to the ISO column 
D = LifeExpect.set_index(['ISO'])
print D.describe()

# In[ ]:
# E. Grabbing data for Gross national income per capita (GNI) 'WHS9_93' 
# Values are per capita purchasing power parity (PPP) int. $ 

import E_GNI
GNI_PPP = E_GNI.getGNI()
# Removing null values 
GNI_PPP = GNI_PPP[GNI_PPP.ISO.notnull()] 
#reseting the index to the ISO Column 
E = GNI_PPP.set_index(['ISO'])
print E.describe()

# In[ ]:
# F. Grabbing data for Net primary school enrolment ratio (Prim) 'WHS9_87' 
# By percent (%)

import F_prim
PrimaryED = F_prim.getPrim()
#removing null values 
PrimaryED = PrimaryED[PrimaryED.ISO.notnull()]
#reseting the index to the ISO column 
F = PrimaryED.set_index(['ISO'])
#F[['EDFMLE_MLE','ED_FMLE','ED_MLE','EDYEARMLE']] = F[['EDFMLE_MLE','ED_FMLE','ED_MLE','EDYEARMLE']].astype(float)
print F.describe()
# In[ ]:
# G. Grabbing data for cellular subscribers (per 100 population) 'WHS9_CS'
# Data given as a percent (%)

import G_cell
cellphones = G_cell.getCell()
#removing null values 
cellphones = cellphones[cellphones.ISO.notnull()]
#reseting the index to the ISO column 
G = cellphones.set_index(['ISO'])

print G.describe()
# In[ ]:
# H. grabbing data for contraceptive prevalence - modern methods (%) 'cpmo' 
# Data in percent (%)

import H_cpmo
contraceptives = H_cpmo.getcontra()
#removing null values 
contraceptives = contraceptives[contraceptives.ISO.notnull()]
#reseting the index to the ISO column 
H = contraceptives.set_index(['ISO'])

print H.describe()

# In[ ]:
# I. Grabbing data for births attended by skilled health personnel (%) 'MDG_0000000025'
# Data in percent (%)

import I_attend
attend = I_attend.getattend()
#removing null values 
attend = attend[attend.ISO.notnull()]
#reseting the index to the ISO column 
I = attend.set_index(['ISO'])

print I.describe()
# In[ ]:
# J. grabbing data for antenatal care coverage - at least four visits (%) 'whs4_154': 
# Data as a percent (%)  

import J_prenatal
prenatal = J_prenatal.getPrenat()
#removing null values 
prenatal = prenatal[prenatal.ISO.notnull()]
#reseting the index to the ISO column 
J = prenatal.set_index(['ISO'])

print J.describe()

# In[ ]:
# K. Grabbing data for estimates of rates of homicide 'VIOLENCE_HOMICIDERATE'
# Per 100 000 population   

import K_homicide
homicide = K_homicide.gethomicide()
#removing null values 
homicide = homicide[homicide.ISO.notnull()]
#reseting the index to the ISO column 
K = homicide.set_index(['ISO'])

print K.describe()

# In[ ]:
#Concating the data frame togwther using the ISO value
#Creating a list of feature data frames 
pieces = [A, B, C, D, E, F, G, H, I, J, K]

# In[ ]:
# concating features into one dataframe with MMR 
mother = pd.concat(pieces, axis=1, join_axes=[C.index])

# In[ ]:

mother.dtypes

# In[ ]:
# visualizing X and y 
#data_cols = ['MMR%','ABR%', 'AOD_FMLE', 'GNI','Abortion_scale', 'EDFMLE_MLE', 'cell_Subscription']

# scatter matrix of feature columns 
#pd.scatter_matrix(mother[data_cols], figsize=(10, 8))

# heat map 
#import seaborn as sns 
#sns.heatmap(mother[data_cols].corr())


 # In[ ]:

#filling missing values 
mother.fillna(mother.median(), inplace=True)

#checking for missing values 
null_data = mother[mother.isnull().any(axis=1)]
print null_data

# building a features list from the mother dataframe
features = [

]

for row in mother:
    features.append(row)
    
# In[ ]:
mother.describe()
# Running a basic logistic regression using the MMRBinary variable
#MMRBinary if '1' MMR is lower than the global median; if '0' MMR is higher than the global median

feature_cols = ['ABR%', 'Abortion_scale', 'AOD_MLE', 'AOD_FMLE', 'AOD_BTSX', 'GNI', 'ED_FMLE', 'ED_MLE', 'EDFMLE_MLE', 'cell_Subscription', 'contraceptives', 'attend', 'prenat%', 'homicide100K']

# define X and y
X = mother[feature_cols]
y = mother.MMRBinary

# In[ ]:
# train/test split
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)

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







 # In[ ]:

#F.plot(kind='hist',y='EDYEARMLE',figsize=(7,5))




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



'''mother = mother[mother.GNI.notnull()]
mother = mother[mother.AOD_MLE.notnull()]
mother = mother[mother.MMR100K.notnull()]
mother = mother[mother.EDFMLE_MLE.notnull()]
mother = mother[mother.ED_FMLE.notnull()]
mother = mother[mother.cell_Subscription.notnull()]
null_data = mother[mother.isnull().any(axis=1)]'''
