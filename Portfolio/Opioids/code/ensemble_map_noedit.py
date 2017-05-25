
import plotly.plotly as py
import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/1962_2006_walmart_store_openings.csv')
df.head()


# This section defines the layout paramaters for the graph, I am not sure if this is for the whole graph or individual graphs. 
# This section also defines the dictionary that the data for each graph will be stored in 


data = []
layout = dict(
    title = 'New Walmart Stores per year 1962-2006<br>\
Source: <a href="http://www.econ.umn.edu/~holmes/data/WalMart/index.html">\
University of Minnesota</a>',
    # showlegend = False,
    autosize = False,
    width = 1000,
    height = 900,
    hovermode = False,
    legend = dict(
        x=0.7,
        y=-0.1,
        bgcolor="rgba(255, 255, 255, 0)",
        font = dict( size=11 ),
    )
)
# This section organizes the data from the data frame into a layout structure for each graph. 
#The dictionary is highly structured to match the infor needed for a scattergeo plot. It is alos labeled with a geo_key at this time to identify the years 
#The name of the geo_key is included in this section of the code 
# the lat and longitudes here are for each individual graph (aka there are repeated lats and longs for each year)

years = df['YEAR'].unique()

for i in range(len(years)):
    geo_key = 'geo'+str(i+1) if i != 0 else 'geo'
    lons = list(df[ df['YEAR'] == years[i] ]['LON'])
    lats = list(df[ df['YEAR'] == years[i] ]['LAT'])
    # Walmart store data
    data.append(
        dict(
            type = 'scattergeo',
            showlegend=False,
            lon = lons,
            lat = lats,
            geo = geo_key,
            name = years[i],
            marker = dict(
                color = "rgb(0, 0, 255)",
                opacity = 0.5
            )
        )
    )

# This section adds on labels to the small graphs in the ordered structure understood by plotly
# the lat and long here will remain the same because you want the title to be in the same spot in each graph. 
# years[i] returns the specific year that allows you to organize the data, for this I will need to build a feature dictionary to do the same thing
# the data will need to be written in using a differnt type of call statement from found in this code 


    # Year markers
    data.append(
        dict(
            type = 'scattergeo',
            showlegend = False,
            lon = [-78],
            lat = [47],
            geo = geo_key,
            text = [years[i]],
            mode = 'text',
        )
    )
    
# this section creates the dictionary that will determine the overall layout of the ensembled graphs. 
# the geo_keys are hppw all of the data is linked to the layout
# this layout is nested inside the main layout, the geo_key is iterated through this loop 
    
    layout[geo_key] = dict(
        scope = 'usa',
        showland = True,
        landcolor = 'rgb(229, 229, 229)',
        showcountries = False,
        domain = dict( x = [], y = [] ),
        subunitcolor = "rgb(255, 255, 255)",
    )
    

# In[]
def draw_sparkline( domain, lataxis, lonaxis ):
    ''' Returns a sparkline layout object for geo coordinates  '''
    return dict(
        showland = False,
        showframe = False,
        showcountries = False,
        showcoastlines = False,
        domain = domain,
        lataxis = lataxis,
        lonaxis = lonaxis,
        bgcolor = 'rgba(255,200,200,0.0)'
    )



# Stores per year sparkline
layout['geo44'] = draw_sparkline({'x':[0.6,0.8], 'y':[0,0.15]}, \
                                 {'range':[-5.0, 30.0]}, {'range':[0.0, 40.0]} )
data.append(
    dict(
        type = 'scattergeo',
        mode = 'lines',
        lat = list(df.groupby(by=['YEAR']).count()['storenum']/1e1),
        lon = range(len(df.groupby(by=['YEAR']).count()['storenum']/1e1)),
        line = dict( color = "rgb(0, 0, 255)" ),
        name = "New stores per year<br>Peak of 178 stores per year in 1990",
        geo = 'geo44',
    )
)

# Cumulative sum sparkline
layout['geo45'] = draw_sparkline({'x':[0.8,1], 'y':[0,0.15]}, \
                                 {'range':[-5.0, 50.0]}, {'range':[0.0, 50.0]} )
data.append(
    dict(
        type = 'scattergeo',
        mode = 'lines',
        lat = list(df.groupby(by=['YEAR']).count().cumsum()['storenum']/1e2),
        lon = range(len(df.groupby(by=['YEAR']).count()['storenum']/1e1)),
        line = dict( color = "rgb(214, 39, 40)" ),
        name ="Cumulative sum<br>3176 stores total in 2006",
        geo = 'geo45',
    )
)


# In[]
z = 0
COLS = 5
ROWS = 9
for y in reversed(range(ROWS)):
    for x in range(COLS):
        geo_key = 'geo'+str(z+1) if z != 0 else 'geo'
        layout[geo_key]['domain']['x'] = [float(x)/float(COLS), float(x+1)/float(COLS)]
        layout[geo_key]['domain']['y'] = [float(y)/float(ROWS), float(y+1)/float(ROWS)]
        z=z+1
        if z > 42:
            break

fig = { 'data':data, 'layout':layout }


# In[]
print years[0]
print geo_key
for row in data: 
    print row

print layout     
# In[]
py.iplot( fig, filename='US Walmart growth', height=900, width=1000 )