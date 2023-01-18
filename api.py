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
        return requests.get(url).iter_content()

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

stock = Stock()
print(stock.list_stocks())
print(stock.get_historical_price('AAPL'))
