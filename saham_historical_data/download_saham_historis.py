import os
import time
import random
import requests
import pandas as pd
from datetime import datetime

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
]

REFERRERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
    "https://www.duckduckgo.com/",
    "https://www.baidu.com/"
]

def random_sleep(min_time=1, max_time=5):
    time.sleep(random.uniform(min_time, max_time))

def download_file(url, dest, retries=5):
    session = requests.Session()
    for i in range(retries):
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": random.choice(REFERRERS)
        }
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            with open(dest, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully to {dest}")
            return
        elif response.status_code == 429:
            print(f"Rate limited, retrying in {2 ** i} seconds...")
            random_sleep(2 ** i)
        else:
            print(f"Failed to download file, status code: {response.status_code}")
            random_sleep(2)
    print("Failed to download file after retries")

def get_excel_filename():
    today = datetime.today().strftime('%Y%m%d')
    return f"C:\\Users\\nigel\\Documents\\ProjectReborn\\saham_data\\downloads\\Daftar Saham  - {today}.xlsx"

def download_yahoo_finance_data(symbol):
    # Calculate the current timestamp
    current_timestamp = int(time.time())
    
    # Construct the download link
    download_link = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=0&period2={current_timestamp}&interval=1d&events=history&includeAdjustedClose=true"
    print(f"Download link: {download_link}")
    
    # Modify the filename to remove ".JK"
    file_name = symbol.replace(".JK", "") + "_historical_data.csv"
    download_dir = "C:\\Users\\nigel\\Documents\\ProjectReborn\\saham_historical_data\\downloads"
    file_path = os.path.join(download_dir, file_name)

    # Download the CSV file with retries
    download_file(download_link, file_path)
    random_sleep()

def main():
    # Load the Excel file based on today's date
    excel_file = get_excel_filename()
    df = pd.read_excel(excel_file)

    # Extract the "Kode" column
    kode_list = df['Kode']

    # Download the CSV files for all codes
    for kode in kode_list:
        download_yahoo_finance_data(kode + ".JK")

if __name__ == "__main__":
    main()