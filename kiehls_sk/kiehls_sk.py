import undetected_chromedriver as uc
import json
import time
import csv
import os


def get_kiehls_stores():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=145)

    # JSON AND CSV FILE
    json_file = "kiehls_sk/kiehls_stores_slovakia.json"
    csv_file = "kiehls_sk/kiehls_stores_slovakia.csv"

    # CSV Header
    fieldnames = [
        "page_url",
        "location_name",
        "street_address",
        "city",
        "state",
        "zip",
        "country_code",
        "store_number",
        "phone",
        "location_type",
        "latitude",
        "longitude",
        "locator_domain",
        "hours_of_operation",
        "raw_address",
    ]

    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    all_store_id = set()
    all_data_for_json = []

    try:

        # slovakia Cities Longitude and Latitude
        slovakia_cities = [
            {"lat": 48.1486, "lng": 17.1077},
            {"lat": 48.7167, "lng": 21.2500},
            {"lat": 48.9984, "lng": 21.2415},
            {"lat": 49.2231, "lng": 18.7394},
            {"lat": 48.3073, "lng": 18.0845},
            {"lat": 48.7376, "lng": 19.1500},
            {"lat": 48.3774, "lng": 17.5872},
            {"lat": 48.8945, "lng": 18.0444},
            {"lat": 49.0650, "lng": 18.9216},
            {"lat": 49.0553, "lng": 20.3117},
        ]

        for slovakia_city in slovakia_cities:
            # slovakia_city_url = f"https://www.kiehls.pl/on/demandware.store/Sites-kiehls-emea-east-ng-Site/pl_PL/Stores-Search?lat={slovakia_city['lat']}&long={slovakia_city['lon']}&radius=10000&ajax=true"
            slovakia_city_url = f"https://www.kiehls.sk/on/demandware.store/Sites-kiehls-emea-east-ng-Site/sk_SK/Stores-Search?lat={slovakia_city['lat']}&long={slovakia_city["lng"]}&radius=10000&ajax=true"
            #  print("City", slovakia_city_url)
            city_url = f"https://www.kiehls.sk/predajne?lat={slovakia_city['lat']}&long={slovakia_city['lng']}"
            driver.get(slovakia_city_url)
            time.sleep(30)
            #  print(driver, "ddd")
            raw_data = driver.find_element("tag name", "body").text
            #  print("Raw data", raw_data)
            data = json.loads(raw_data)
            #  print("Raw data", data)
            stores = data.get("storelocatorresults", {}).get("stores", [])
            print(" Length", len(stores))

            for store in stores:
                store_id = store["id"]
                if store_id not in all_store_id:
                    all_store_id.add(store_id)
                    data = {
                        "page_url": city_url,
                        "location_name": store["name"] or "Missing",
                        "street_address": store["address1"] or "Missing",
                        "city": store["city"] or "Missing",
                        "state": store["stateCode"] or "Missing",
                        "zip": store["postalCode"] or "Missing",
                        "country_code": store["countryCode"] or "Missing",
                        "store_number": "Missing",
                        "store_number": "Missing",
                        "phone": store["phone"] or "Missing",
                        "location_type": "Missing",
                        "latitude": (
                            str(store["latitude"]) if store["latitude"] else "Missing"
                        ),
                        "longitude": (
                            str(store["longitude"]) if store["longitude"] else "Missing"
                        ),
                        "locator_domain": "kiehls.sk",
                        "hours_of_operation": store["hours"] or "Missing",
                        "raw_address": (
                            f"{store['address1']}, {store['city']}"
                            if store["address1"]
                            else "Missing"
                        ),
                    }
                    with open(csv_file, "a", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writerow(data)
                    all_data_for_json.append(data)
                    print(f"   ✅ Saved New Store: {data['location_name']}")

        # Save JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(all_data_for_json, f, ensure_ascii=False, indent=4)

        print(f"Total Stores: {len(all_data_for_json)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    get_kiehls_stores()
