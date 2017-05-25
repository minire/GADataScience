import pandas as pd
import numpy as py

path = "../dataincubator/"
CMS = pd.read_csv(path + 'PartD_Prescriber_PUF_NPI_14.csv') 

CMS.head()

for columns in CMS:
    print columns


CMS.BENE_COUNT. mean()



CMS['prescription_length'] = CMS.TOTAL_DAY_SUPPLY/CMS.TOTAL_CLAIM_COUNT
CMS['prescription_length'].describe()

#calculting median
CMS['prescription_length'].median()
CMS.head()


#checking if number makes sense 
# histogram of prescription lengths 
import matplotlib.pyplot as plt

%matplotlib inline 
CMS.plot(kind='hist', y='prescription_length', figsize=(7,5))

#recalculating the median 

CMSort = CMS.sort_values(by = ['prescription_length'])
CMSort.head(32750)
#29.286223

# determining fraction of name brand drugs by speciality 

CMS.BRAND_CLAIM_COUNT.describe()
CMS.GENERIC_CLAIM_COUNT.describe()
CMS.TOTAL_CLAIM_COUNT.describe()

CMS.groupby('SPECIALTY_DESCRIPTION').mean().TOTAL_CLAIM_COUNT

#Create a new data frame by speciality           
CMSSpeciality = CMS.groupby('SPECIALTY_DESCRIPTION').mean()
CMSSpeciality.describe()

#Creating a subset of Specialties with 1000 or more drug claims
CMSS1000 = CMSSpeciality[CMSSpeciality['TOTAL_CLAIM_COUNT'] >= 1000]
CMSS1000.describe()
CMSS1000['drugratioB_G'] = CMSS1000['BRAND_CLAIM_COUNT']/CMSS1000['TOTAL_CLAIM_COUNT']
CMSS1000.drugratioB_G.std()


# determining ratio of opioid prescriptions to anibiotic prescriptions
CMSState = CMS.groupby('NPPES_PROVIDER_STATE').mean()
CMSState.ANTIBIOTIC_BENE_COUNT.describe()
CMSState['RatioO_A'] = CMSState['OPIOID_BENE_COUNT']/CMSState['ANTIBIOTIC_BENE_COUNT']

#sorting Values by ratio
CMSState.sort_values(by = ['RatioO_A'])
#determining the difference between STATES with the largest and smallest Ratio 
CMSState.RatioO_A.NV - CMSState.RatioO_A.NY

TOTAL_CLAIM_COUNT