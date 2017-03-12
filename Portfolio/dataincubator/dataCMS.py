import pandas as pd
import numpy as py

path = "../dataincubator/"
CMS = pd.read_csv(path + 'PartD_Prescriber_PUF_NPI_14.csv') 

CMS.head()

for columns in CMS:
    print columns

#CMS.describe()
#total = CMS.TOTAL_DAY_SUPPLY.median()
#claims = CMS.TOTAL_CLAIM_COUNT.median()


CMS['prescription_length'] = CMS.TOTAL_DAY_SUPPLY/CMS.TOTAL_CLAIM_COUNT
CMS['prescription_length']describe()
CMS.head()


# histogram of prescription lengths 
import matplotlib.pyplot as plt

%matplotlib inline 
CMS.plot(kind='hist', y='TOTAL_DAY_SUPPLY', figsize=(7,5))
