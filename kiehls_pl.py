from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
# Updated URL for 2026 store locator
# url = "
url = "https://www.kiehls.pl/znajdz-sklep"  # Direct link to store locator

try:
    driver.get(url)
    wait = WebDriverWait(driver, 15)

    html_source = driver.page_source

    file_path = "html_content.html"

    with open(file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_source)
    print(f"HTML file '{file_path}' has been created successfully.")


finally:
    driver.quit()
