from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
# Updated URL for 2026 store locator
# url = "
url = "https://www.kiehls.pl" # Direct link to store locator

try:
    driver.get(url)
    wait = WebDriverWait(driver, 15)

    # 1. Handle Cookie Banner (Essential for visibility)
    try:
        cookie_accept = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        cookie_accept.click()
    except Exception:
        print("Cookie banner not found or already closed.")

    # 2. Trigger store loading (Search for 'Warszawa' to populate the list)
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search'], .pac-target-input")))
    search_input.send_keys("Warszawa")
    search_input.send_keys(Keys.ENTER)

    # 3. Use a broader selector for the store list
    # As of 2026, Kiehl's often uses 'div[data-role="store-item"]' or '.store-tile'
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".store-list, .store-tile-container")))

    # 4. Extract all matching store elements
    stores = driver.find_elements(By.CSS_SELECTOR, ".store-tile, .store-item")
    print(f"Successfully extracted {len(stores)} stores.")

    for s in stores:
        print(s.text)
        print("-" * 20)

finally:
    driver.quit()
