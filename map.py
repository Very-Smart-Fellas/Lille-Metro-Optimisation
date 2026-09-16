import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import json
from shapely.geometry import LineString
import folium

# Data filtering

try:
    with open("data/json/filtered_data.json", "r") as file:
        data = json.load(file)
    with open("data/json/filtered_routes.json", "r") as file:
        routes = json.load(file)
    with open("data/json/filtered_trips.json", "r") as file:
        trips = json.load(file)
    with open("data/json/filtered_stop_times.json", "r") as file:
        stop_times = json.load(file)
    with open("data/json/filtered_stops.json", "r") as file:
            stops = json.load(file)

except:
    routes = pd.read_csv("data/gtfs/routes.txt")
    trips = pd.read_csv("data/gtfs/trips.txt")
    stop_times = pd.read_csv("data/gtfs/stop_times.txt")
    stops = pd.read_csv("data/gtfs/stops.txt")

    routes = routes[["route_type", "route_short_name", "route_id"]].values.tolist()
    routes = [route for route in routes if route[0] == 0 or route[0] == 1]

    trips = trips[["route_id", "trip_id"]].values.tolist()
    trips = [trip for trip in trips if trip[0] in [route[2] for route in routes]]

    stop_times = stop_times[["trip_id", "stop_id", "stop_sequence"]].values.tolist()
    stop_times = [stop_time for stop_time in stop_times if stop_time[0] in [trip[1] for trip in trips]]

    stops = stops[["stop_id", "stop_name", "stop_lat", "stop_lon"]].values.tolist()
    stops = [stop for stop in stops if stop[0] in [stop_time[1] for stop_time in stop_times]]

    data = {
        "stop_id": [stop[0] for stop in stops],
        "stop_name": [stop[1] for stop in stops],
        "stop_lat": [stop[2] for stop in stops],
        "stop_lon": [stop[3] for stop in stops],
        "route_type": [],
        "route_short_name": [],
        "stop_sequence": [],
        "trip_id": []
    }

    for i in tqdm(range(len(stops))):
        found = False
        for j in range(len(stop_times)):
            if stops[i][0] == stop_times[j][1]:
                for k in range(len(trips)):
                    if stop_times[j][0] == trips[k][1]:
                        for l in range(len(routes)):
                            if trips[k][0] == routes[l][2]:
                                data["route_type"].append(routes[l][0])
                                data["route_short_name"].append(routes[l][1])
                                data["stop_sequence"].append(stop_times[j][2])
                                data["trip_id"].append(trips[k][1])
                                found = True
                                break
                        if found:
                            break
                if found:
                    break
        if not found:
            data["route_type"].append(None)
            data["route_short_name"].append(None)
            data["stop_sequence"].append(None)

    with open("data/json/filtered_data.json", "w") as file:
        json.dump(data, file)
    with open("data/json/filtered_routes.json", "w") as file:
        json.dump(routes, file)
    with open("data/json/filtered_trips.json", "w") as file:
        json.dump(trips, file)
    with open("data/json/filtered_stop_times.json", "w") as file:
        json.dump(stop_times, file)
    with open("data/json/filtered_stops.json", "w") as file:
        json.dump(stops, file)

me1 = {
    "stop_id": [],
    "stop_name": [],
    "stop_lat": [],
    "stop_lon": [],
    "route_type": [],
    "route_short_name": [],
    "stop_sequence": [],
    "trip_id": []
    }
me2 = {
    "stop_id": [],
    "stop_name": [],
    "stop_lat": [],
    "stop_lon": [],
    "route_type": [],
    "route_short_name": [],
    "stop_sequence": [],
    "trip_id": []
    }
tram = {
    "stop_id": [],
    "stop_name": [],
    "stop_lat": [],
    "stop_lon": [],
    "route_type": [],
    "route_short_name": [],
    "stop_sequence": [],
    "trip_id": []
    }

for i in range(len(data["stop_id"])):
    if data["route_short_name"][i] == "M1":
        me1["stop_id"].append(data["stop_id"][i])
        me1["stop_name"].append(data["stop_name"][i])
        me1["stop_lat"].append(data["stop_lat"][i])
        me1["stop_lon"].append(data["stop_lon"][i])
        me1["route_type"].append(data["route_type"][i])
        me1["route_short_name"].append(data["route_short_name"][i])
        me1["stop_sequence"].append(data["stop_sequence"][i])
        me1["trip_id"].append(data["trip_id"][i])
    elif data["route_short_name"][i] == "M2":
        me2["stop_id"].append(data["stop_id"][i])
        me2["stop_name"].append(data["stop_name"][i])
        me2["stop_lat"].append(data["stop_lat"][i])
        me2["stop_lon"].append(data["stop_lon"][i])
        me2["route_type"].append(data["route_type"][i])
        me2["route_short_name"].append(data["route_short_name"][i])
        me2["stop_sequence"].append(data["stop_sequence"][i])
        me2["trip_id"].append(data["trip_id"][i])
    elif data["route_short_name"][i] == "TRAM":
        tram["stop_id"].append(data["stop_id"][i])
        tram["stop_name"].append(data["stop_name"][i])
        tram["stop_lat"].append(data["stop_lat"][i])
        tram["stop_lon"].append(data["stop_lon"][i])
        tram["route_type"].append(data["route_type"][i])
        tram["route_short_name"].append(data["route_short_name"][i])
        tram["stop_sequence"].append(data["stop_sequence"][i])
        tram["trip_id"].append(data["trip_id"][i])

def get_data():
    print(f"Number of routes: {len(data["routes"])}")
    print(f"Number of trips: {len(data["trips"])}")
    print(f"Number of stop_times: {len(data["stop_times"])}")
    print(f"Number of stops: {len(data["stops"])}")


# Data mapping

me1df = pd.DataFrame(me1)
me2df = pd.DataFrame(me2)
tramdf = pd.DataFrame(tram)

for df in [me1df, me2df, tramdf]:
    df[['stop_lat', 'stop_lon']] = df[['stop_lat', 'stop_lon']].apply(pd.to_numeric, errors='coerce')
    df.dropna(subset=['stop_lat', 'stop_lon'], inplace=True)

me1_stops = gpd.GeoDataFrame(
    me1df,
    geometry=gpd.points_from_xy(me1df.stop_lon, me1df.stop_lat),
    crs="EPSG:4326"
)

me2_stops = gpd.GeoDataFrame(
    me2df,
    geometry=gpd.points_from_xy(me2df.stop_lon, me2df.stop_lat),
    crs="EPSG:4326"
)

tram_stops = gpd.GeoDataFrame(
    tramdf,
    geometry=gpd.points_from_xy(tramdf.stop_lon, tramdf.stop_lat),
    crs="EPSG:4326"
)

esri_url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
esri_attr = "Esri"

m = me1_stops.explore(
    color="yellow",
    marker_kwds=dict(radius=6),
    tooltip=["stop_name", "stop_sequence"],
    popup=True,
    tiles=esri_url,
    attr=esri_attr,
    name = "ME1"
)

me2_stops.explore(
    m=m,
    color="red",
    marker_kwds=dict(radius=6),
    tooltip=["stop_name", "stop_sequence"],
    popup=True,
    tiles=esri_url,
    attr=esri_attr,
    name = "ME2"
)

tram_stops.explore(
    m=m,
    color="blue",
    marker_kwds=dict(radius=6),
    tooltip=["stop_name", "stop_sequence"],
    popup=True,
    tiles=esri_url,
    attr=esri_attr,
    name = "TRAM"
)

me1df = me1df[me1df["trip_id"] == me1df["trip_id"].dropna().iloc[0]].sort_values(by="stop_sequence")
me2df = me2df[me2df["trip_id"] == me2df["trip_id"].dropna().iloc[0]].sort_values(by="stop_sequence")
tramdf = tramdf[tramdf["trip_id"] == tramdf["trip_id"].dropna().iloc[0]].sort_values(by="stop_sequence")

coords = list(zip(me1df.stop_lon, me1df.stop_lat))
if len(coords) > 1:
    me1_line = LineString(coords)

coords = list(zip(me2df.stop_lon, me2df.stop_lat))
if len(coords) > 1:
    me2_line = LineString(coords)

coords = list(zip(tramdf.stop_lon, tramdf.stop_lat))
if len(coords) > 1:
    tram_line = LineString(coords)

routes_gdf = gpd.GeoDataFrame({
    'route_name': ['ME1', 'ME2', 'TRAM'],
    'geometry': [me1_line, me2_line, tram_line]
}, crs="EPSG:4326")

routes_gdf.explore(
    m=m,
    column="route_name",
    cmap=["yellow", "red", "blue"], # Colors match your point colors
    style_kwds={'weight': 5},       # Line thickness
    tooltip=["route_name"],
    name="Route Lines"
)

m.save("interactive_stops_map.html")