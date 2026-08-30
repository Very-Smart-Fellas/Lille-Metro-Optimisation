import pandas as pd
import json

try:
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

    stop_times = stop_times[["trip_id", "stop_id"]].values.tolist()
    stop_times = [stop_time for stop_time in stop_times if stop_time[0] in [trip[1] for trip in trips]]

    stops = stops[["stop_id", "stop_name", "stop_lat", "stop_lon"]].values.tolist()
    stops = [stop for stop in stops if stop[0] in [stop_time[1] for stop_time in stop_times]]

    with open("data/json/filtered_routes.json", "w") as file:
        json.dump(routes, file)
    with open("data/json/filtered_trips.json", "w") as file:
        json.dump(trips, file)
    with open("data/json/filtered_stop_times.json", "w") as file:
        json.dump(stop_times, file)
    with open("data/json/filtered_stops.json", "w") as file:
        json.dump(stops, file)

print (f"Number of routes: {len(routes)}")
print (f"Number of trips: {len(trips)}")
print (f"Number of stop_times: {len(stop_times)}")
print (f"Number of stops: {len(stops)}")