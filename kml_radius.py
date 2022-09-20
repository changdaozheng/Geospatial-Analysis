#Construct circles around target coordinates to identify areas within a certain distance 
from polycircles import polycircles
import pandas as pd 
import simplekml

df = pd.read_csv("")#Input Raw File that contains Lat and Lng columns
new_df = df.dropna(axis= 0 , subset=['Lat', 'Lng'])

def draw_circle(name, lat, lng):
    polycircle = polycircles.Polycircle(latitude=lat,
                                        longitude=lng,
                                        radius=200,
                                        number_of_vertices=36)
    pol = kml.newpolygon(name=name, outerboundaryis=polycircle.to_kml())
    pol.style.polystyle.color = simplekml.Color.rgb(255,140,0,60) #https://htmlcolorcodes.com/
   

kml = simplekml.Kml()
for i in range(len(new_df.index)):
    draw_circle(new_df.iloc[i, """Name Column"""], new_df.iloc[i, """Latitude Column"""], new_df.iloc[i, """Longitude Column"""])
    
kml.save(".kml") #Save Output as kml file