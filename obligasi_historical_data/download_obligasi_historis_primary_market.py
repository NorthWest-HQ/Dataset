import requests
import pandas as pd
import os
import time
import random

# Define the URLs and headers
url_data = "https://www.bca.co.id/api/bca/Funds/GetData"
url_info = "https://www.bca.co.id/api/bca/Funds/GetData"
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "X-Kl-Kis-Ajax-Request": "Ajax_Request",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,id;q=0.8,fr;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "Origin": "https://www.bca.co.id",
    "Referer": "https://www.bca.co.id/",
    "Connection": "keep-alive",
}

# Function to simulate human behavior by adding random delays
def human_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))

# Read the bond codes from the input CSV file
bond_codes_df = pd.read_csv(r"C:\Users\nigel\Documents\ProjectReborn\obligasi_data\downloads\bond_code_secondary_market.csv")
bond_codes = bond_codes_df['bond_code'].tolist()

# Process each bond code
for bond_code in bond_codes:
    print(f"Processing bond code: {bond_code}")
    
    # Define the payloads
    payload_data_percentage = {
        "code": "Obligasi.GrafikJualBeli",
        "parameters[0][key]": "p_enum",
        "parameters[0][value]": "price_sell",
        "parameters[1][key]": "p_product_code",
        "parameters[1][value]": bond_code,
        "parameters[2][key]": "p_start_date",
        "parameters[2][value]": "01/01/2014",
        "parameters[3][key]": "p_end_date",
        "parameters[3][value]": "25/05/2024",
    }

    payload_data_yield = {
        "code": "Obligasi.GrafikJualBeli",
        "parameters[0][key]": "p_enum",
        "parameters[0][value]": "yield_buy",
        "parameters[1][key]": "p_product_code",
        "parameters[1][value]": bond_code,
        "parameters[2][key]": "p_start_date",
        "parameters[2][value]": "01/01/2014",
        "parameters[3][key]": "p_end_date",
        "parameters[3][value]": "25/05/2024",
    }

    payload_data_buy = {
        "code": "Obligasi.GrafikJualBeli",
        "parameters[0][key]": "p_enum",
        "parameters[0][value]": "price_buy",
        "parameters[1][key]": "p_product_code",
        "parameters[1][value]": bond_code,
        "parameters[2][key]": "p_start_date",
        "parameters[2][value]": "01/01/2014",
        "parameters[3][key]": "p_end_date",
        "parameters[3][value]": "25/05/2024",
    }

    payload_info = {
        "code": "Obligasi.InformasiProduk",
        "parameters[0][key]": "p_product_code_list",
        "parameters[0][value]": bond_code,
        "parameters[1][key]": "p_product_code_list",
        "parameters[1][value]": bond_code,
    }

    # Send the POST requests with human-like delays
    print("Sending request for price percentage data...")
    response_data_percentage = requests.post(url_data, headers=headers, data=payload_data_percentage)
    print("Response status code for price percentage data:", response_data_percentage.status_code)
    human_delay()

    print("Sending request for yield data...")
    response_data_yield = requests.post(url_data, headers=headers, data=payload_data_yield)
    print("Response status code for yield data:", response_data_yield.status_code)
    human_delay()

    print("Sending request for buy percentage data...")
    response_data_buy = requests.post(url_data, headers=headers, data=payload_data_buy)
    print("Response status code for buy percentage data:", response_data_buy.status_code)
    human_delay()

    print("Sending request for bond information...")
    response_info = requests.post(url_info, headers=headers, data=payload_info)
    print("Response status code for bond information:", response_info.status_code)
    human_delay()

    # Check if the requests were successful
    if response_data_percentage.status_code == 200 and response_data_yield.status_code == 200 and response_data_buy.status_code == 200 and response_info.status_code == 200:
        print("All requests successful. Parsing responses...")

        # Parse the JSON responses
        data_percentage = response_data_percentage.json().get('data', [])
        data_yield = response_data_yield.json().get('data', [])
        data_buy = response_data_buy.json().get('data', [])
        info = response_info.json().get('data', [])[0]
        
        print("Extracting price percentage data...")
        # Extract the required information
        sell_percentage_data = [(item.get('price_date'), item.get('price_value')) for item in data_percentage]
        
        print("Extracting yield data...")
        yield_value_data = {item.get('price_date'): item.get('price_value') for item in data_yield}
        
        print("Extracting buy percentage data...")
        buy_percentage_data = {item.get('price_date'): item.get('price_value') for item in data_buy}
        
        print("Combining data...")
        # Combine the data into a single dataframe
        combined_data = []
        for date, sell_percentage in sell_percentage_data:
            yield_value = yield_value_data.get(date, None)
            buy_percentage = buy_percentage_data.get(date, None)
            if yield_value is not None and buy_percentage is not None:
                combined_data.append((date, sell_percentage, buy_percentage, yield_value))
        
        df = pd.DataFrame(combined_data, columns=['price_date', 'sell_percentage', 'buy_percentage', 'yield_value'])
        
        # Define the file path and name
        obligasi_cd = info.get('obligasi_cd')
        file_path = os.path.join(r"C:\Users\nigel\Documents\ProjectReborn\obligasi_historical_data\downloads\secondary_market", f"{obligasi_cd}_historical_data.csv")
        
        print(f"Saving data to {file_path}...")
        # Save the dataframe as a CSV file
        df.to_csv(file_path, index=False)
        
        print(f"Data saved to {file_path}")

    else:
        print(f"Failed to retrieve data for bond code {bond_code}. Status codes: {response_data_percentage.status_code}, {response_data_yield.status_code}, {response_data_buy.status_code}, {response_info.status_code}")