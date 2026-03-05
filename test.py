poland_cities = [
     {"lat": 52.2297, "lon": 21.0122},
     {"lat": 50.0647, "lon": 19.9450},
    {"lat": 51.7592, "lon": 19.4560},
     {"lat": 51.1079, "lon": 17.0385},
     {"lat": 52.4064, "lon": 16.9252},
    {"lat": 54.3520, "lon": 18.6466},
     {"lat": 53.4285, "lon": 14.5528},
     {"lat": 53.1235, "lon": 18.0084},
     {"lat": 51.2465, "lon": 22.5684},
     {"lat": 50.2649, "lon": 19.0238},
     {"lat": 53.1325, "lon": 23.1688},
     {"lat": 54.5189, "lon": 18.5305},
     {"lat": 50.8118, "lon": 19.1204},
    {"lat": 51.4026, "lon": 21.1471},
     {"lat": 53.0138, "lon": 18.5984}
]

# print("Poland cities", poland_cities)

for city in poland_cities:
    print(city["lat"], city["lon"])