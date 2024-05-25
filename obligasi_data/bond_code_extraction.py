import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from random import randint

# Configure Selenium options
options = Options()
options.add_argument("--headless")  # Run headless for efficiency and avoiding detection
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument('--log-level=3')  # Suppress console logs

# Initialize the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to extract product codes from a given URL and XPath
def extract_product_codes(url, xpath, product_split, file_path, remove_prefix=None):
    driver.get(url)
    time.sleep(5)

    # Human-like behavior: scroll slowly through the page
    for i in range(3):
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(randint(2, 5))

    # Find the table body containing the bond data
    try:
        table_body = driver.find_element(By.XPATH, xpath)
        print(f"Table body found at {url}.")
    except Exception as e:
        print(f"Error finding table body at {url}: {e}")
        return

    # Extract all the product codes from the href attributes in the anchor tags
    product_codes = []
    try:
        rows = table_body.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            link = row.find_element(By.TAG_NAME, "a")
            href = link.get_attribute("href")
            product_code = href.split(product_split)[1]
            if remove_prefix:
                product_code = product_code.replace(remove_prefix, "")
            product_codes.append(product_code)
        print(f"Extracted {len(product_codes)} product codes from {url}.")
    except Exception as e:
        print(f"Error extracting product codes from {url}: {e}")
        return

    # Write the product codes to a CSV file
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["bond_code"])
            for code in product_codes:
                writer.writerow([code])
        print(f"Product codes saved to {file_path}.")
    except Exception as e:
        print(f"Error writing to CSV file at {file_path}: {e}")

# Extract product codes from the secondary market
secondary_market_url = "https://www.bca.co.id/id/individu/produk/investasi-dan-asuransi/obligasi/pilihan-produk-obligasi"
secondary_market_xpath = '/html/body/div[5]/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody'
secondary_market_file_path = r'C:\Users\nigel\Documents\ProjectReborn\obligasi_data\downloads\bond_code_secondary_market.csv'
extract_product_codes(secondary_market_url, secondary_market_xpath, "product=", secondary_market_file_path)

# Extract product codes from the primary market
primary_market_url = "https://www.bca.co.id/id/individu/produk/investasi-dan-asuransi/obligasi/pasar-perdana"
primary_market_xpath = '/html/body/div[5]/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody'
primary_market_file_path = r'C:\Users\nigel\Documents\ProjectReborn\obligasi_data\downloads\bond_code_primary_market.csv'
extract_product_codes(primary_market_url, primary_market_xpath, "/obligasi/pasar-perdana/", primary_market_file_path, "obligasi-")

# Close the browser
driver.quit()