import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np
import plotly.graph_objects as go
from scipy import optimize as opt
from IPython.display import display
import time

def objective_func(location,points_coords,points_weights):
    x = location[0]    #location is a 1d array containing the latitude and longitude of the facility
    y = location[1]
    x_i = points_coords[:,0]    #points_coords in a 2d array of shape (n,2) where n in the number of cities, it contains the latitudes and longitudes of the cities
    y_i = points_coords[:,1]
    w_i = points_weights    #points_coords in a 2d array of shape (n,2) where n in the number of cities, it contains the population size of the cities  
    return sum((abs((x_i-x))+abs((y_i-y))*w_i))
    
'''
data = pd.read_excel("Brescia_province_data.xlsx",sep = ";") #loads the excel file containing the cities and their population
display(data.head())

geoloc = Nominatim(user_agent="Facility_loc_problem")
coordinates_df = pd.DataFrame(np.zeros((len(data.index),2)),index = data.index, columns = ["lat","long"])
cities = data.loc[:,"City"].values
i = 0
while i != (len(cities)): #gets the latitude and longitude of every point
    try:
        location = geoloc.geocode(cities[i] + ", Brescia, Italy")
        coordinates_df.loc[i,"lat"] = location.latitude 
        coordinates_df.loc[i,"long"] = location.longitude
        i+=1
        time.sleep(1)
    except:
        time.sleep(20)
        continue
data = data.join(coordinates_df)
display(data.head())
data.to_csv("Brescia_province_data_complete.csv",sep = ";")
'''
#Uncomment the code above to retrieve the latitudes and longitudes of the cities

data = pd.read_csv("Brescia_province_data_complete.csv",sep = ";",index_col = 0)
fig = go.Figure(go.Scattermapbox(lat=data.loc[:,"lat"],
                                 lon=data.loc[:,"long"],
                                 text = data.loc[:,"City"],
                                marker_size = 8))
fig.update_layout(mapbox_style="open-street-map")
fig.show()

location = [0,0] #our starting latitude and longitude points for the facility
coordinates_df = data.loc[:,["lat","long"]]
res = opt.minimize(objective_func,location,args = (coordinates_df.values, data.loc[:,"Pop size"].values),method ="Nelder-Mead", tol = 10**(-9))
location = res.x
print("The latitude and the longitude of the optimal location is = " + str((res.x[0],res.x[1])))
geoloc = Nominatim(user_agent="Facility_loc_prodblem")
print(geoloc.reverse(location))
fig = go.Figure(go.Scattermapbox(lat=data.loc[:,"lat"],
                                 lon=data.loc[:,"long"],
                                 name = "Cities",
                                 text = data.loc[:,"City"],
                                 marker_size = 8))
fig.add_trace(go.Scattermapbox(lat = [location[0]],
                               lon = [location[1]],
                               marker_color =  "green",
                               name = "Facility",
                               marker_size = 12))
fig.update_layout(mapbox_style="open-street-map")
fig.show()