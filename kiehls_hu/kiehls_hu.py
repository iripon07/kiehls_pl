import undetected_chromedriver as uc
import json
import time
import csv
import os


def get_kiehls_stores():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=145)

    # JSON AND CSV FILE
    json_file = "kiehls_hu/kiehls_stores_hungary.json"
    csv_file = "kiehls_hu/kiehls_stores_hungary.csv"

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

        # Hungary Cities Longitude and Latitude
        hungary_cities = [
            {"lat": 47.4979, "lng": 19.0402},
            {"lat": 47.5316, "lng": 21.6273},
            {"lat": 46.2530, "lng": 20.1414},
            {"lat": 48.1039, "lng": 20.7785},
            {"lat": 46.0727, "lng": 18.2323},
            {"lat": 47.6833, "lng": 17.6351},
            {"lat": 47.9554, "lng": 21.7169},
            {"lat": 46.9062, "lng": 19.6913},
            {"lat": 47.1930, "lng": 18.4107},
            {"lat": 47.2309, "lng": 16.6216},
        ]

        for hungary_city in hungary_cities:
            hungary_city_url = f"https://www.kiehls.hu/on/demandware.store/Sites-kiehls-emea-east-ng-Site/hu_HU/Stores-Search?lat={hungary_city['lat']}&long={hungary_city['lng']}&radius=10000&ajax=true"
            city_url = f"https://www.kiehls.hu/%C3%BCzletek?lat={hungary_city['lat']}&long={hungary_city['lng']}"
            driver.get(hungary_city_url)
            time.sleep(30)
            raw_data = driver.find_element("tag name", "body").text
            data = json.loads(raw_data)
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
                        "locator_domain": "kiehls.hu",
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
