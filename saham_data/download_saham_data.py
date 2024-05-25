import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def random_sleep(min_time=1, max_time=3):
    time.sleep(random.uniform(min_time, max_time))

def download_saham_data():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    
    # Set download directory preferences
    download_dir = "C:\\Users\\nigel\\Documents\\ProjectReborn\\saham_data\\downloads\\saham"  # Ensure this directory exists
    prefs = {"download.default_directory": download_dir}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.idx.co.id/id/data-pasar/data-saham/daftar-saham")

        # Mimic human behavior: Scroll down the page a bit
        driver.execute_script("window.scrollTo(0, 300);")
        random_sleep()

        # Wait for the download button to be clickable
        wait = WebDriverWait(driver, 20)
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/main/div/div[1]/div/div[4]/button')))
        
        # Ensure the element is in view
        driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
        random_sleep()

        print("Download button located. Attempting to click...")
        
        # Use JavaScript click
        driver.execute_script("arguments[0].click();", download_button)
        
        # Wait for the download to complete (this may vary based on your internet speed)
        time.sleep(20)  # Adjust the sleep time as necessary

        print("Download completed successfully")

        # Verify the file is downloaded
        files = os.listdir(download_dir)
        if files:
            print(f"Downloaded files: {files}")
        else:
            print("No files found in the download directory.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    download_saham_data()