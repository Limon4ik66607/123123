import aiohttp
import asyncio
import json
from settings import get_collection_data  # Импортируйте функцию для получения данных о коллекции
from datetime import datetime

API_URL = 'https://api.getgems.io/graphql'

headers = {
    "Content-Type": "application/json"
}

async def fetch_data(session, query, variables=None):
    async with session.post(API_URL, headers=headers, json={"query": query, "variables": variables}) as response:
        if response.status == 200:
            return await response.json()
        else:
            raise Exception(f"Request failed with status {response.status}: {await response.text()}")

async def fetch_nft_data(session, collection_address):
    query = f"""
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
          }}
        }}
      }}
    }}
    """
    return await fetch_data(session, query)

async def fetch_nft_sales_data(session, collection_address):
    query = """
    query Items($collectionAddress: String!) {
      historyCollectionSales(collectionAddress: $collectionAddress) {
        items {
          date
        }
      }
    }
    """
    variables = {"collectionAddress": collection_address}
    return await fetch_data(session, query, variables)

def nanoto_ton(nano_amount):
    return nano_amount / 1_000_000_000  # 1 ton = 10^9 nano

def print_nft_data(nft_data, sales_data):
    sales_dates = {item['date'] for item in sales_data['data']['historyCollectionSales']['items']}
    
    if 'data' not in nft_data or 'nftCollectionItems' not in nft_data['data']:
        print("No data found in the response.")
        return

    items = nft_data['data']['nftCollectionItems']['items']
    for item in items:
        creation_time = None
        for attr in item['attributes']:
            if attr['traitType'] == 'Date':
                try:
                    creation_time = datetime.fromtimestamp(int(attr['value']))
                except ValueError as e:
                    print(f"Error parsing date: {e}")
                break

        if creation_time:
            creation_timestamp = int(creation_time.timestamp())
            if creation_timestamp in sales_dates:
                print(f"Name: {item['name']}")
                print(f"Address: {item['address']}")
                print(f"Index: {item['index']}")
                if item['sale']:
                    price_in_ton = nanoto_ton(int(item['sale']['fullPrice']))
                    print(f"Price: {price_in_ton:.4f} TON")
                print(f"Creation Date: {creation_time.strftime('%d %b, %I:%M %p')}")
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
                print("-" * 20)

async def handle_update(call):
    try:
        # Сохранение текущего времени при запуске скрипта
        start_time = datetime.now()

        # Получаем user_id из объекта вызова
        user_id = call.from_user.id
        
        # Получаем collection_name и collection_address из настроек
        collection_name = '1'  # Измените на реальное получение имени коллекции
        collection_data = get_collection_data(user_id, collection_name)
        
        if collection_data:
            collection_address = collection_data['address']
            async with aiohttp.ClientSession() as session:
                nft_data_task = fetch_nft_data(session, collection_address)
                sales_data_task = fetch_nft_sales_data(session, collection_address)
                
                nft_data, sales_data = await asyncio.gather(nft_data_task, sales_data_task)
                
                print(json.dumps(nft_data, indent=2))  # Добавляем вывод необработанного ответа
                print(json.dumps(sales_data, indent=2))  # Вывод необработанного ответа о продажах
                print_nft_data(nft_data, sales_data)
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
    asyncio.run(handle_update(test_call))
