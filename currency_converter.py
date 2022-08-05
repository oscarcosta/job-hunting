import json
from datetime import datetime
from exchange_api import ExchangeAPIClient


class CurrencyConverter:

    def __init__(self, base_currency, to_currencies):
        self.__api_key = self.__read_api_key('data/api_key.txt')
        self.__exchange_file = 'data/exchange_latest.json'
        self.exchange_data = None
        self.fetch_exchange_rates(base_currency, to_currencies)

    @staticmethod
    def __read_api_key(api_key_file):
        with open(api_key_file, 'r') as reader:
            api_key = reader.readline().rstrip()
        return api_key

    def __read_exchange_file(self):
        with open(self.__exchange_file, 'r') as reader:
            data = reader.read()
        return json.loads(data)

    def __write_exchange_file(self, json_data):
        with open(self.__exchange_file, 'w') as writer:
            writer.write(json.dumps(json_data))

    @staticmethod
    def __is_data_valid(exchange_data, base_currency, to_currencies):
        valid = exchange_data['base'] == base_currency  # same base currency?
        if valid:
            rates = exchange_data['rates'].keys()
            valid = all(elem in rates for elem in to_currencies)  # contains all currencies?
        if valid:
            data_timestamp = datetime.fromtimestamp(exchange_data['timestamp'])
            diff = data_timestamp - datetime.today()
            valid = diff.days < 1  # is current?
        return valid

    def fetch_exchange_rates(self, base_currency, to_currencies):
        self.exchange_data = self.__read_exchange_file()
        if not self.__is_data_valid(self.exchange_data, base_currency, to_currencies):
            print('Fetching exchange rates for ', base_currency, to_currencies)
            api = ExchangeAPIClient(self.__api_key)
            self.exchange_data = api.fetch_latest(base_currency, ','.join(to_currencies))
            self.__write_exchange_file(self.exchange_data)

    def convert_to_base(self, amount, currency):
        amount = float(amount)
        if amount != amount or currency == '' or currency == self.exchange_data['base']:
            return amount
        # convert
        rate = self.exchange_data['rates'][currency]
        return amount / rate
