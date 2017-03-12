import pandas as pd
import numpy as py

path = "../dataincubator/"
CMS = pd.read_csv(path + 'PartD_Prescriber_PUF_NPI_14.csv') 
drug_poisoning = pd.read_csv(path + 'drug_poisoning_deaths_by_state-_us_2013_2014-v7.csv')
CMS.head()
drug_poisoning.head()

for columns in CMS:
    print columns

#CMS.describe()
#total = CMS.TOTAL_DAY_SUPPLY.median()
#claims = CMS.TOTAL_CLAIM_COUNT.median()


CMS['prescription_length'] = CMS.TOTAL_DAY_SUPPLY/CMS.TOTAL_CLAIM_COUNT
CMS['prescription_length'].describe()
CMS.head()


# histogram of prescription lengths 
import matplotlib.pyplot as plt

%matplotlib inline 
CMS.plot(kind='hist', y='prescription_length', figsize=(7,5))

# Group by state 
CMS.groupby('NPPES_PROVIDER_STATE').OPIOID_BENE_COUNT.mean().sort_values()
CMS.groupby('NPPES_PROVIDER_STATE').TOTAL_CLAIM_COUNT.mean()

CMSopioid = CMS.groupby('NPPES_PROVIDER_STATE').OPIOID_BENE_COUNT.mean()
CMSOP = pd.DataFrame(CMSopioid) 
CMStotal = CMS.groupby('NPPES_PROVIDER_STATE').TOTAL_CLAIM_COUNT.mean()
CMSTOT = pd.DataFrame(CMStotal)

CMSOpioids = pd.concat([CMSOP, CMSTOT],axis=1)
CMSOpioids['propopiods'] = CMSOpioids['OPIOID_BENE_COUNT']/CMSOpioids['TOTAL_CLAIM_COUNT']

CMSOpioids['propopiods'].sort_values()

CMS.boxplot(column='OPIOID_CLAIM_COUNT', by='NPPES_PROVIDER_STATE', figsize=(20,6))
CMS.boxplot(column='TOTAL_CLAIM_COUNT', by='NPPES_PROVIDER_STATE', showfliers=False, figsize=(20,6))
CMSOpioids.boxplot(column='propopiods', figsize=(20,6))
NPPES_PROVIDER_STATE
# select features
