import requests


API_URL = "https://financialmodelingprep.com/api/v3/"

def get_json(url):
    """
    Get json from url
    """
    url = API_URL + url + '?apikey='
    return requests.get(url).json()

def list_stocks():
    """
    List all stocks
    """
    url = 'stock/list'
    return get_json(url)

def get_historical_price(symbol):
    """
    Get historical price for
    a specific stock symbol
    """
    url = 'historical-price-full/' + symbol
    return get_json(url)['historical']
