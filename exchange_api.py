import requests


class ExchangeAPIClient:

    def __init__(self, api_key):
        self.__url_latest = 'https://api.apilayer.com/exchangerates_data/latest'
        self.__api_key = api_key

    def fetch_latest(self, base_currency, symbols):
        response = requests.get(self.__url_latest,
                                params={'base': base_currency, 'symbols': symbols},
                                headers={'apikey': self.__api_key})
        if response.status_code == 200:
            print('Successfully fetched data')
            return response.json()
        else:
            print(f'Error fetching data. Error code {response.status_code}.')
