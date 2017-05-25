import pandas as pd
import numpy as np 

# Import activity data for Jun, Jul, and August.
path = "../yammer/"
yammer = pd.read_csv(path + 'yammercreatedJJA.csv')
yammer.head()
yammer.describe()

# convert objects to datetime 
yammer.activated_at = pd.to_datetime(yammer.activated_at)
yammer.created_at = pd.to_datetime(yammer.created_at) 

yammer['created'] = yammer['created_at']
yammer = yammer.set_index('created_at')
yammer = yammer.resample('1D').count()

%matplotlib inline
import matplotlib.pyplot as plt


#plt.plot(yammer.index, yammer.activated_at)

x = yammer.index
y1 = yammer.created 
y2 = yammer.activated_at 

plt.figure(figsize=(10,5))
plt.fill(x, y1, 'o', alpha=0.3)
plt.show()


plt.figure(figsize=(10,5))
plt.fill(x, y2, 'b', alpha=0.3)
plt.show()


fig, ax = plt.subplots(figsize=(10,5))
ax.fill(x, y1, 'o', x, y2, 'b', alpha=0.3)
plt.show()