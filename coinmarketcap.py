import json
import properties
import requests

coin_dictionary = {}
INITIAL_COUNT_VAL = 0

def ingest_coin_listing():
    headers = {'X-CMC_PRO_API_KEY': properties.coinmarketcap_api_key,
            'Accept': 'application/json'}

    response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=250&convert=USD',
                        headers=headers)
    
    print(json.dumps(response.json(), indent=4))

    return response

def process_data(coin_listing):
    print("hello")
    for coin in coin_listing.json()['data']:
        dictionary_key1 = coin['name'].lower()
        dictionary_key2 = coin['symbol'].lower()
        coin_dictionary[(dictionary_key1, dictionary_key2)] = INITIAL_COUNT_VAL
    
    return coin_dictionary

#print(coin_dictionary)


#coin_listing = ingest_coin_listing()
#process_data(coin_listing)
