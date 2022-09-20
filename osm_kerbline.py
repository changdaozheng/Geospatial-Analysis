#import and init all packages
import pandas as pd 
import overpy
import requests
import folium 
import osmnx 
import math

api = overpy.Overpass()


def main():
    #Bounding Box for target area 
    bounding_box = (1.2723568, 103.8417435, 1.285113, 103.850834)
    box_south = bounding_box[0]
    box_west = bounding_box[1]
    box_north = bounding_box[2]
    box_east = bounding_box[3]

    #Produce digraph from osmnx
    graph = osmnx.graph_from_bbox(box_north, box_south, box_east, box_west, network_type= "drive_service", simplify=True, retain_all=False, truncate_by_edge=False, clean_periphery=True, custom_filter=None) #network_type options : {"all_private", "all", "bike", "drive", "drive_service", "walk"}
    nodes, streets = osmnx.graph_to_gdfs(graph)


    #Plot graph of all connected networks 
    #osmnx.folium.plot_graph_folium(graph)

    for ways in streets['osmid']:
        if type(ways) == list:
            for way in ways: 
                query_way(way)
        elif type(ways) == int: 
            query_way(ways)
    



#Updates dataframe with more information about nodes in a way 
def query_way(way):
  global df
  result = api.query("""
      way({});
      (._;>;);
      out body;
      """.format(way))
  
  for way in result.ways:
    for node in range(len(way.nodes)):
      
      name = way.tags.get("name", "n/a")
      way_id = way.id
      node_id = way.nodes[node].id
      highway = way.tags.get('highway', 'n/a')
      lat = way.nodes[node].lat
      lng = way.nodes[node].lon
      
      if node < len(way.nodes) - 1 :
        next_lat = way.nodes[node + 1].lat
        next_lng = way.nodes[node + 1].lon
        bearing = get_bearing(lat, lng, next_lat, next_lng)
      else: 
        bearing = None

      df = df.append({"way": way,"name": name , "way_id": way_id,"node_id":node_id,"highway": highway, "lat": lat, "lng":lng, 'bearing': bearing}, ignore_index = True)


#Update bearings of a road
def get_bearing(startLat, startLng, endLat, endLng):
    startLat = math.radians(startLat)
    startLong = math.radians(startLng)
    endLat = math.radians(endLat)
    endLong = math.radians(endLng)

    dLong = endLong - startLong

    dPhi = math.log(math.tan(endLat/2.0+math.pi/4.0)/math.tan(startLat/2.0+math.pi/4.0))
    if abs(dLong) > math.pi:
        if dLong > 0.0:
            dLong = -(2.0 * math.pi - dLong)
        else:
            dLong = (2.0 * math.pi + dLong)

    bearing = (math.degrees(math.atan2(dLong, dPhi)) + 360.0) % 360.0

    return bearing


main()