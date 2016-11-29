'''
CLASS: Getting Maternal Mortality rates form WHO- GHO


'''

# Link to the global health observatory API description page
#http://apps.who.int/gho/data/node.resources.api

# Look through the API description links and examples to see what use you have avaialble



# Use the requests library to interact with a URL


import pandas as pd 

# importing maternal mortality rate as a .csv file and looking at the head of the dataframe
path = "../data/"
mat_mor = pd.read_csv(path + 'maternalMortalityRate.csv')   
mat_mor.head()

# testing the drop function 
mat_mor.drop(['GHO (DISPLAY)'], axis=1, inplace=True)
mat_mor.head()

#removing unecessary/extra features
mat_mor.drop(['GHO (URL)','PUBLISHSTATE (CODE)', 'PUBLISHSTATE (DISPLAY)', 'PUBLISHSTATE (URL)','YEAR (CODE)','YEAR (URL)', 'REGION (DISPLAY)', 'REGION (URL)', 'COUNTRY (URL)', 'Display Value', 'Comments'], axis=1, inplace=True)
mat_mor.head()

#removing old maternal mortality rates 

mat_mor = mat_mor.rename(columns = {'GHO (CODE)': 'TYPE', 'YEAR (DISPLAY)': 'YEAR','REGION (CODE)': 'REGION','COUNTRY (CODE)': 'CNTRY', 'COUNTRY (DISPLAY)': 'COUNTRY'})
mat_mor.head()

# creating a new datafrome by removing the total number of deaths by country; maintaining only the rate of deaths per 100K live births 
mat_mor_rate = mat_mor[mat_mor.TYPE == 'MDG_0000000026']
mat_mor_rate.head()



# creating a new maternal mortality dataframe that only contains data from 2015 
mat_mor15 = mat_mor_rate[mat_mor_rate.YEAR == 2015]
mat_mor15.head()        

#looking at basic stats of mat_mor15 dataframe
mat_mor15.describe()        
mat_mor15.sort('COUNTRY')
mat_mor15.groupby('REGION').mean()


#indexing dataframe by country 
indexed_MMR = mat_mor15.set_index(['COUNTRY']) 
indexed_MMR.drop(['TYPE'], axis=1, inplace=True)
indexed_MMR.head()
indexed_MMR.describe()


#importing Human development index data 
path = "../data/"
HDI = pd.read_csv(path + 'HDI_UN_2014.csv')   
HDI.head()


# rename country by to COUNTRY and make this the index 
HDI['COUNTRY']  = HDI ['Country']
HDI.drop(['Country', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'], axis=1, inplace=True)
indexed_HDI = HDI.set_index(['COUNTRY'])
indexed_HDI.head()
HDI.describe()


# conactenating maternal mortality rate and human development index 
MMR_HDI = pd.concat([indexed_MMR, indexed_HDI], axis=1)
MMR_HDI = MMR_HDI.rename(columns = {'Numeric': 'Numeric_MMR', 'Low' : 'Low_MMR', 'High' : 'High_MMR'})
MMR_HDI.dtypes

#finding missing values 
null_data = MMR_HDI[MMR_HDI.isnull().any(axis=1)]
print null_data


# basic statistics for human development index and maternal mortality rate 
import seaborn as sns

MMR_HDI['GNI'] = MMR_HDI['GNI'].convert_objects(convert_numeric=True)
MMR_HDI.dtypes
MMR_HDI = MMR_HDI.rename(columns = {'GNI': 'GNI_PPP'})

# basic graphing of data 
#heatmap
sns.heatmap(MMR_HDI.corr())
# scatter plot matrix (0=red, 1=green, 2=blue)
pd.scatter_matrix(MMR_HDI, figsize=(10,10), s=10)

# searching for data on a specific country 
MMR_HDI.loc['Albania']  



#importing data for births attended by a health professional (DATA INCOMPLETE) 
path = "../data/"
professionalbirth = pd.read_csv(path + 'births attended by a health professional.csv')   
professionalbirth.head()
professionalbirth.describe()

#Importing health outcomes data 
path = "../data/"
healthOutcomes = pd.read_csv(path + 'healthOutcomes_UN.csv')   
healthOutcomes.head()
healthOutcomes.describe()

#importing national income and resources 
path = "../data/"
NationalIncome = pd.read_csv(path + 'National income and resources.csv')   
NationalIncome.head()
NationalIncome.describe()



#Gender Inequality Index 
path = "../data/"
GII = pd.read_csv(path + 'GenderInequalityIndex_UN.csv')   
GII.head()

#importing adolescent birth rate 
path = "../data/"
Adolbr = pd.read_csv(path + 'MDG_0000000003_adolescent birth rate.csv')
adolbr.head()



#importing aceess to abortion data 



#importing violence against women data 
