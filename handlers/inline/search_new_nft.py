import requests
import json
from settings import get_collection_data  # Импортируйте функцию для получения данных о коллекции

API_URL = 'https://api.getgems.io/graphql'

headers = {
    "Content-Type": "application/json"
}

def fetch_nft_data(collection_address):
    print("Sending request to API...")
    body = f"""
    query {{
      nftCollectionItems (address: "{collection_address}", first: 100) {{
        items {{
          name
          address
          index
          sale {{
            ... on NftSaleFixPrice {{
              fullPrice
            }}
          }}
          rarityAttributes {{
            traitType
            value
          }}
          owner {{
            name
            wallet
            socialLinks {{
              url
            }}
            description
          }}
          attributes {{
            traitType
            value
            displayType
            date 
          }}
        }}
      }}
    }}
    """
    response = requests.post(API_URL, headers=headers, data=json.dumps({"query": body}))
    print(f"Received response with status code: {response.status_code}")
    if response.status_code == 200:
        print("Parsing JSON response...")
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}")
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {response.text}")

def nanoto_ton(nano_amount):
    return nano_amount / 1_000_000_000  # 1 ton = 10^9 nano

def print_nft_data(nft_data):
    if 'data' not in nft_data or 'nftCollectionItems' not in nft_data['data']:
        print("No data found in the response.")
        return

    items = nft_data['data']['nftCollectionItems']['items']
    for item in items:
        print(f"Name: {item['name']}")
        print(f"Address: {item['address']}")
        print(f"Index: {item['index']}")
        if item['sale']:
            price_in_ton = nanoto_ton(int(item['sale']['fullPrice']))  # Ensure fullPrice is an integer
            print(f"Price: {price_in_ton:.4f} TON")  # Format to 4 decimal places
        if item['rarityAttributes']:
            print("Rarity Attributes:")
            for attr in item['rarityAttributes']:
                print(f"  {attr['traitType']}: {attr['value']}")
        if item['owner']:
            print(f"Owner Name: {item['owner']['name']}")
            print(f"Owner Wallet: {item['owner']['wallet']}")
            if item['owner']['socialLinks']:
                print("Social Links:")
                for link in item['owner']['socialLinks']:
                    print(f"  {link['url']}")
            print(f"Owner Description: {item['owner']['description']}")
        if 'attributes' in item:
            for attr in item['attributes']:
                if attr['traitType'] == 'Date':  # Проверяем тип атрибута
                    date = attr['value']
                    print(f"Created At: {date}")  # Отобразите время добавления
        print("-" * 20)

