import undetected_chromedriver as uc
import json
import time
import sys


# item = {
#         "page_url": "Missing",
#         "location_name": "Missing",
#         "street_address": "Missing",
#         "city": "Missing",
#         "state": "Missing",
#         "zip": "Missing",
#         "country_code": "Missing",
#         "store_number": "Missing",
#         "phone": "Missing",
#         "location_type": "Missing",
#         "latitude": "Missing",
#         "longitude": "Missing",
#         "locator_domain": "kiehls.pl",
#         "hours_of_operation": "Missing",
#         "raw_address": "Missing"
# }

def get_stores_reliably():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=145)
    
    try:

        # Poland Cities Longitude and Latitude
        poland_cities = [
            {"lat": 52.2297, "lon": 21.0122},
            # {"lat": 50.0647, "lon": 19.9450},
            # {"lat": 51.7592, "lon": 19.4560},
            # {"lat": 51.1079, "lon": 17.0385},
            # {"lat": 52.4064, "lon": 16.9252},
            # {"lat": 54.3520, "lon": 18.6466},
            # {"lat": 53.4285, "lon": 14.5528},
            # {"lat": 53.1235, "lon": 18.0084},
            # {"lat": 51.2465, "lon": 22.5684},
            # {"lat": 50.2649, "lon": 19.0238},
            # {"lat": 53.1325, "lon": 23.1688},
            # {"lat": 54.5189, "lon": 18.5305},
            # {"lat": 50.8118, "lon": 19.1204},
            # {"lat": 51.4026, "lon": 21.1471},
            # {"lat": 53.0138, "lon": 18.5984}
            ]
        
        for poland_city in poland_cities:
            poland_city_url = f"https://www.kiehls.pl/on/demandware.store/Sites-kiehls-emea-east-ng-Site/pl_PL/Stores-Search?lat={poland_city['lat']}&long={poland_city['lon']}&radius=10000&ajax=true"
            #  print("City", poland_city_url)
            driver.get(poland_city_url)
            time.sleep(30)
            #  print(driver, "ddd")
            raw_data = driver.find_element("tag name", "body").text
            #  print("Raw data", raw_data)
            data = json.loads(raw_data)
            #  print("Raw data", data)
            stores = data.get("storelocatorresults", {}).get("stores", [])
            # print(" Length", len(stores))

            for store in stores:
                data = {
                    "page_url": "https://www.kiehls.pl/sklepy",
                    "location_name": store("name") or "Missing",
                    "street_address": store("address1") or "Missing",
                    "city": store("city") or "Missing",
                    "state": store("stateCode") or "Missing",
                    "zip": store("postalCode") or "Missing",
                    "country_code": store("countryCode") or "Missing",
                    # "store_number": str(sid),
                    "store_number": "Missing",
                    "phone": store("phone") or "Missing",
                    "location_type": "Missing",
                    "latitude": str(store("latitude")) if store("latitude") else "Missing",
                    "longitude": str(store("longitude")) if store("longitude") else "Missing",
                    "locator_domain": "kiehls.pl",
                    "hours_of_operation": store("hours") or "Missing",
                    "raw_address": f"{store('address1')}, {store('city')}" if store("address1") else "Missing",
        }
                name = store["name"]
                city = store["city"]
                latitude = store["latitude"]
                print("Name", name)
                print("City", city)
                print("Latitude", latitude)
                print("-" * 30)

                
            # for index, store in enumerate(stores, 1):
            #     name = store.get("name")
            #     city = store.get("city")
            #     address = store.get("address1")
            #     phone = store.get("phone")
        
            #     print(f"{index}. {name}")
            #     print(f"   📍 Address: {address}, {city}")
            #     print(f"   📞 Phone:   {phone}")
            #     print("-" * 30)
            
        
    finally:
        driver.quit()

if __name__ == "__main__":
    get_stores_reliably()