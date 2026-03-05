import undetected_chromedriver as uc
import json
import time
import sys

def get_stores_reliably():
    options = uc.ChromeOptions()
    # options.add_argument('--headless') # Keep this commented out so you can see it work!
    
    print("🚀 Starting browser...")
    driver = uc.Chrome(options=options, version_main=145)
    
    try:
        # STEP 1: Visit the main page to get "Valid Session Cookies"
        print("🔗 Step 1: Visiting homepage to get cookies...")
        driver.get("https://www.kiehls.pl/sklepy")
        time.sleep(6) # Give it time to solve the "I am human" challenge
        
        # STEP 2: Request the API while the session is active
        # We use a real coordinate (Warsaw) and a wide radius
        api_url = "https://www.kiehls.pl/on/demandware.store/Sites-kiehls-emea-east-ng-Site/pl_PL/Stores-Search?lat=52.2302&long=21.0026&radius=5000&ajax=true"
        
        print("📡 Step 2: Requesting API with active session...")
        driver.get(api_url)
        time.sleep(4)
        
        # STEP 3: Grab the data
        raw_content = driver.find_element("tag name", "body").text
        
        if raw_content.strip().startswith('{'):
            data = json.loads(raw_content)
            stores = data.get('stores', [])
            
            if not stores and 'storelocatorresults' in data:
                stores = data['storelocatorresults'].get('stores', [])
            
            print(f"\n✅ SUCCESS! Found {len(stores)} stores.")
            
            # Save the file immediately
            with open('kiehls_stores_final.json', 'w', encoding='utf-8') as f:
                json.dump(stores, f, ensure_ascii=False, indent=4)
            
            for s in stores:
                print(f"📍 {s.get('name')} - {s.get('city')}")
        else:
            print("❌ Still blocked. The page is showing HTML, not JSON.")
            print("Response starts with:", raw_content[:50])

    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        driver.quit()
        sys.exit(0)

if __name__ == "__main__":
    get_stores_reliably()