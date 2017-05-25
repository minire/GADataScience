import pandas as pd
import numpy as np 

# Import activity data for Jun, Jul, and August.
path = "../yammer/"
yammer = pd.read_csv(path + 'yammerJJAactivity.csv')
yammer.head()
yammer.describe()

# convert objects to datetime 
yammer.activated_at = pd.to_datetime(yammer.activated_at)
yammer.created_at = pd.to_datetime(yammer.created_at) 
yammer.occurred_at = pd.to_datetime(yammer.occurred_at) 

#yammerCreate = yammer.groupby(yammer.user_id)
#yammerCreate.describe()

yammer['activation_time'] = yammer['activated_at'] - yammer['created_at']
yammer.head()
yammer.activation_time.describe()
yammer.activation_time = pd.to_numeric(yammer.activation_time)
yammerCreated = yammer.activation_time.groupby(yammer.user_id).() 
yammerCreated.head()

%matplotlib inline
import matplotlib.pyplot as plt
plt.plot(yammer.yammer.created_at, )
