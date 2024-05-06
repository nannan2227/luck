 

import requests
import csv

# 配置项
ETHERSCAN_API_KEY = ' '  # 请替换成你的Etherscan API密钥
ETHERSCAN_API_URL = 'https://api.etherscan.io/api'
INPUT_FILE = '11.txt'
OUTPUT_FILE = 'result.csv'

def get_gas_total(address):
    try:
        response = requests.get(ETHERSCAN_API_URL, params={
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'sort': 'asc',
            'apikey': ETHERSCAN_API_KEY
        })
        data = response.json()

        # Check if the API response includes an error message
        if 'status' in data and data['status'] == '0':
            print(f"Error from Etherscan API for address {address}: {data['message']}")
            return None
        
        # Check if the 'result' field is present and is a list
        if 'result' in data and isinstance(data['result'], list):
            transactions = data['result']
            total_gas_used = sum(int(tx['gasUsed']) * int(tx['gasPrice']) for tx in transactions)
        else:
            print(f"Unexpected JSON structure for address {address}")
            return None
        
        # Calculate the total ETH consumed
        total_eth_consumed = total_gas_used / (10**18)  # Convert Wei to ETH
        return round(total_eth_consumed, 4)
    except Exception as e:
        print(f"Error fetching gas for address {address}: {e}")
        return None

def main():
    with open(INPUT_FILE, 'r') as file:
        addresses = [line.strip() for line in file.readlines()]

    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        fieldnames = ['Address', 'TotalETHConsumed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for address in addresses:
            total_eth_consumed = get_gas_total(address)
            if total_eth_consumed is not None:
                writer.writerow({'Address': address, 'TotalETHConsumed': total_eth_consumed})
                print(f"Address: {address}, Total ETH consumed: {total_eth_consumed}")

if __name__ == "__main__":
    main()
