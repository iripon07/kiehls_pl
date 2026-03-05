import undetected_chromedriver as uc
import json
import time
import csv
import os


def get_kiehls_stores():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=145)

    # JSON AND CSV FILE
    json_file = "kiehls_bg/kiehls_stores_bulgaria.json"
    csv_file = "kiehls_bg/kiehls_stores_bulgaria.csv"

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

        # bulgaria Cities Longitude and Latitude
        bulgaria_cities = [
            {"lat": 42.6977, "lng": 23.3219},
            {"lat": 42.1354, "lng": 24.7453},
            {"lat": 43.2141, "lng": 27.9147},
            {"lat": 42.5048, "lng": 27.4626},
            {"lat": 43.8356, "lng": 25.9656},
            {"lat": 42.4258, "lng": 25.6338},
        ]

        for bulgaria_city in bulgaria_cities:
            bulgaria_city_url = f"https://www.kiehls.bg/on/demandware.store/Sites-kiehls-emea-east-ng-Site/bg_BG/Stores-Search?lat={bulgaria_city['lat']}&long={bulgaria_city['lng']}&radius=10000&ajax=true"
            city_url = f"https://www.kiehls.bg/%D0%BF%D0%BE%D1%82%D1%8A%D1%80%D1%81%D0%B5%D1%82%D0%B5-%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD?lat={bulgaria_city['lat']}&long={bulgaria_city['lng']}"
            driver.get(bulgaria_city_url)
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
                        "locator_domain": "kiehls.bg",
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
