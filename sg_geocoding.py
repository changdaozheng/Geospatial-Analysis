#Geocoding for Singapore Postal codes with the use of OneMap API
import requests 
import json 
import pandas as pd 
from time import sleep

link = 'https://developers.onemap.sg/commonapi/search?searchVal={searchVal}&returnGeom=Y&getAddrDetails=N&pageNum=1'

def geocode(postal_code):
    try:
        result = requests.get(link.format(searchVal=postal_code))
        data = json.loads(result.content)

        lat = data['results'][0]['LATITUDE']
        lng = data['results'][0]['LONGTITUDE']
        sleep(0.241) #250 requests per minute
        return [lat, lng]

    except Exception as e:
        return ["NA", "NA"]

df = pd.read_csv("", dtype='object')#Enter File Name 
#df = pd.read_excel("")
Lat = []
Lng = []

num_postcodes = df[''].size #Name of Column with zipcode/postal code
for i in range(num_postcodes):
    zipcode = str(df[''][i])#Name of Column with zipcode/postal code
    if len(zipcode) < 6 :
        zipcode = "0"+zipcode
    arr = geocode(postal_code = zipcode)
    print("{}   {} {}\n".format(i, arr[0], arr[1]))
    Lat.append(arr[0])
    Lng.append(arr[1])

try:
    df['Lat'] = Lat
    df['Lng'] = Lng
except Exception as e:
    print(e)

print(df.head())
df.to_csv(".csv", index=False) #Enter Output File Name
#df.to_excel(".csv", index=False)