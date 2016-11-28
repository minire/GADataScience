import plotly.plotly as py
import plotly.graph_objs as go 
import numpy as np
import pandas as pd 

N = 40
x = np.linspace(0, 1, N)
y = np.random.randn(N)
data_store1 = pd.DataFrame({'x':x, 'y':y})

data = [
    go.Bar(
        x=data_store1['Date'],
        y=data_store1['Sales']
    )
]

url = py.plot(data, filename='pandas-bar-chart')