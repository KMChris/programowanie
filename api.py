from dotenv import load_dotenv
import pandas as pd
import requests
import os

load_dotenv()
API_URL = 'https://financialmodelingprep.com/api/'
API_KEY = os.environ.get('API_KEY')

INTERVALS = ['1min', '5min', '15min', '30min', '1hour', '4hour', 'day']
OUTPUT_TYPES = ['json', 'pandas']

class API:

    def __init__(self, output='pandas'):
        if output not in OUTPUT_TYPES:
            raise ValueError('Invalid output type')
        if API_KEY is None:
            raise ValueError('API key not found')
        self.output = output

    def _get_data(self, url, key=None):
        """
        Get Pandas DataFrame or JSON from API
        for a given URL

        Parameters
        ----------
        url : str
            URL to get data from
        key : str or None
            Evaluate item from JSON
            or return full JSON if None

        Returns
        -------
        pandas.DataFrame or dict
            Dataframe or JSON
        """
        url = API_URL + url + '?apikey=' + API_KEY
        json = requests.get(url).json()
        if key:
            json = json[key]
        if self.output == 'pandas':
            return pd.DataFrame(json)
        return json

    def list_category(self, category):
        """
        List symbols from a specific category

        Parameters
        ----------
        category : str
            Category to list symbols from

        Returns
        -------
        pandas.DataFrame or dict
            Dataframe or JSON with symbols and names
        """
        if category == 'stocks':
            url = 'v3/stock/list'
        elif category == 'crypto':
            url = 'v3/symbol/available-cryptocurrencies'
        elif category == 'forex':
            url = 'v3/symbol/available-forex-currency-pairs'
        elif category == 'commodities':
            url = 'v3/symbol/available-forex-currency-pairs'
        else:
            raise ValueError('Invalid category')
        return self._get_data(url)

    def get_historical(self, symbol, interval='day'):
        """
        Get historical prices and volume for
        a specific stock, cryptocurrency,
        forex or commodity symbol and
        a given interval
        """
        if interval not in INTERVALS:
            raise ValueError('Invalid interval')
        if interval == 'day':
            url = f'v3/historical-price-full/{symbol}'
            data = self._get_data(url, 'historical')
            return data.sort_values('date')
        url = f'v3/historical-chart/{interval}/{symbol}'
        data = self._get_data(url)
        return data.sort_values('date')

    def get_historical_capitalization(self, symbol):
        """
        Get historical capitalization for
        a specific stock symbol
        """
        url = f'v3/historical-market-capitalization/{symbol}'
        return self._get_data(url)

if __name__ == "__main__":
    api = API()
    print(api.list_stocks())
    print(api.get_historical('AAPL', '1min'))
