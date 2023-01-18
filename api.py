from dotenv import load_dotenv
import pandas as pd
import requests, os

load_dotenv()
API_URL = "https://financialmodelingprep.com/api/"
API_KEY = os.environ.get("API_KEY")

class Stock:
    """
    Stock class
    """

    @staticmethod
    def _get_json(url):
        """
        Get json from url
        """
        url = API_URL + url + '?apikey=' + API_KEY
        return requests.get(url).json()

    @classmethod
    def list_stocks(cls):
        """
        List all stocks
        """
        url = API_URL + 'v3/stock/list' + '?apikey=' + API_KEY
        return requests.get(url)

    @classmethod
    def list_crypto(cls):
        """
        List all cryptocurrencies
        """
        url = API_URL + 'v3/symbol/available-cryptocurrencies' + '?apikey=' + API_KEY
        return requests.get(url)

    @classmethod
    def list_forex(cls):
        """
        List all forex
        """
        url = API_URL + 'v3/symbol/available-forex-currency-pairs' + '?apikey=' + API_KEY
        return requests.get(url)

    @classmethod
    def list_comodities(cls):
        """
        List all commodities
        """
        url = API_URL + 'v3/symbol/available-commodities' + '?apikey=' + API_KEY
        return requests.get(url)

    @classmethod
    def get_historical_price(cls, symbol):
        """
        Get historical price for
        a specific stock symbol
        """
        url = 'v3/historical-price-full/' + symbol
        return cls._get_json(url)['historical']

    @classmethod
    def get_historical_capitalization(cls, symbol):
        """
        Get historical capitalization for
        a specific stock symbol
        """
        url = 'v3/historical-market-capitalization/{symbol}'
        return cls._get_json(url)['historical']

    @classmethod
    def get_historical(cls, symbol, interval='1min'):
        """
        Get historical prices for
        a specific cryptocurrency,
        forex or commodity symbol
        and given interval
        """
        if interval == 'day':
            url = 'v3/historical-price-full/{symbol}'
        else:
            url = 'v3/historical-chart/{interval}/{symbol}'
        return cls._get_json(url)['historical']

if __name__=="__main__":
    stock = Stock()
    print(stock.list_stocks())
    print(stock.get_historical_price('AAPL'))
