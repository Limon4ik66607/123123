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
            displayType
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
        print(f"Name: {item.get('name', 'N/A')}")
        print(f"Address: {item.get('address', 'N/A')}")
        print(f"Index: {item.get('index', 'N/A')}")
        
        sale = item.get('sale', {})
        if sale:
            price_in_ton = nanoto_ton(int(sale.get('fullPrice', 0)))
            print(f"Price: {price_in_ton:.4f} TON")
        else:
            print("Price: N/A")
        
        rarity_attributes = item.get('rarityAttributes', [])
        if rarity_attributes:
            print("Rarity Attributes:")
            for attr in rarity_attributes:
                print(f"  {attr.get('traitType', 'N/A')}: {attr.get('value', 'N/A')}")
        else:
            print("Rarity Attributes: None")

        owner = item.get('owner', {})
        print(f"Owner Name: {owner.get('name', 'N/A')}")
        print(f"Owner Wallet: {owner.get('wallet', 'N/A')}")
        if owner.get('socialLinks'):
            print("Social Links:")
            for link in owner.get('socialLinks', []):
                print(f"  {link.get('url', 'N/A')}")
        else:
            print("Social Links: None")
        print(f"Owner Description: {owner.get('description', 'N/A')}")
        
        attributes = item.get('attributes', [])
        for attr in attributes:
            if attr.get('displayType') == 'Date':  # Проверяем тип отображения
                date = attr.get('value', 'N/A')
                print(f"Created At: {date}")
        
        print("-" * 20)

def handle_update(call):
    try:
        # Получаем user_id из объекта вызова
        user_id = call.from_user.id
        
        # Получаем collection_name и collection_address из настроек
        collection_name = '1'  # Измените на реальное получение имени коллекции
        collection_data = get_collection_data(user_id, collection_name)
        
        if collection_data:
            collection_address = collection_data['address']
            nft_data = fetch_nft_data(collection_address)
            print(json.dumps(nft_data, indent=2))  # Добавляем вывод необработанного ответа
            print_nft_data(nft_data)
        else:
            print(f"Collection '{collection_name}' not found for user '{user_id}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Для тестирования функции handle_update можно использовать тестовый вызов.
    class FakeCall:
        class FakeUser:
            def __init__(self, user_id):
                self.id = user_id
        def __init__(self, user_id):
            self.from_user = self.FakeUser(user_id)

    test_call = FakeCall(user_id='5070172256')
    handle_update(test_call)
