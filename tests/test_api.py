import api as api_module
from unittest.mock import patch
import pandas as pd
import pytest

def test_get_data():
    api_module.API_URL = 'test_url/'
    api_module.API_KEY = 'test_key'
    api = api_module.API()

    # Test case when output is 'pandas' and key is not None
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            'key1': {
                'col1': [1, 2],
                'col2': [3, 4]
            }
        }
        df = api._get_data(url='URL', key='key1')
        mock_get.assert_called_with('test_url/URL?apikey=test_key')
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ['col1', 'col2']
        assert list(df.col1) == [1, 2]
        assert list(df.col2) == [3, 4]

    # Test case when output is 'pandas' and key is None
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            'key1': {
                'col1': [1, 2],
                'col2': [3, 4]
            }
        }
        df = api._get_data(url='URL')
        mock_get.assert_called_with('test_url/URL?apikey=test_key')
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ['key1']
        assert list(df.key1) == [[1, 2], [3, 4]]

    # Test case when output is 'json' and key is not None
    api.output = 'json'
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            'key1': {
                'col1': [1, 2],
                'col2': [3, 4]
            }
        }
        df = api._get_data(url='URL', key='key1')
        mock_get.assert_called_with('test_url/URL?apikey=test_key')
        assert isinstance(df, dict)
        assert list(df.keys()) == ['col1', 'col2']
        assert list(df['col1']) == [1, 2]
        assert list(df['col2']) == [3, 4]

    # Test case when output is 'json' and key is None
    api.output = 'json'
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            'key1': {
                'col1': [1, 2],
                'col2': [3, 4]
            }
        }
        df = api._get_data(url='URL')
        mock_get.assert_called_with('test_url/URL?apikey=test_key')
        assert isinstance(df, dict)
        assert list(df.keys()) == ['key1']
        assert list(df['key1']) == ['col1', 'col2']

    # Test case when API_KEY is invalid
    api_module.API_KEY = 'invalid'
    api = api_module.API()
    with pytest.raises(ValueError):
        api._get_data('v3/stock/list', 'symbol')

def test_list_category():
    data = [
        {
            'symbol': 'AAPL',
            'name': 'Apple Inc.'
        },
        {
            'symbol': 'MSFT',
            'name': 'Microsoft Corporation'
        }
    ]
    api = api_module.API()
    api._get_data = lambda x: pd.DataFrame(data)

    # Test case when category is 'stocks'
    result = api.list_category('stocks')
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['symbol', 'name']
    assert list(result.symbol) == ['AAPL', 'MSFT']
    assert list(result.name) == ['Apple Inc.', 'Microsoft Corporation']

    # Test case when category is 'crypto'
    result = api.list_category('crypto')
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['symbol', 'name']
    assert list(result.symbol) == ['AAPL', 'MSFT']
    assert list(result.name) == ['Apple Inc.', 'Microsoft Corporation']

    # Test case when category is 'forex'
    result = api.list_category('forex')
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['symbol', 'name']
    assert list(result.symbol) == ['AAPL', 'MSFT']
    assert list(result.name) == ['Apple Inc.', 'Microsoft Corporation']

    # Test case when category is 'commodities'
    result = api.list_category('commodities')
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['symbol', 'name']
    assert list(result.symbol) == ['AAPL', 'MSFT']
    assert list(result.name) == ['Apple Inc.', 'Microsoft Corporation']

    # Test case when category is invalid
    with pytest.raises(ValueError) as e:
        api.list_category('invalid')
    assert str(e.value) == 'Invalid category'

def test_get_historical():
    # Test case when interval is 'day'
    data = {
        'historical': {
            'date': ['2022-01-01', '2022-01-02'],
            'close': [100, 110]
        }
    }
    api = api_module.API()
    api._get_data = lambda x, y: pd.DataFrame(data[y])
    result = api.get_historical('AAPL')
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['date', 'close']
    assert list(result.date) == ['2022-01-01', '2022-01-02']
    assert list(result.close) == [100, 110]

    # Test case when interval is not 'day'
    data = {
        'date': ['2022-01-01', '2022-01-02'],
        'close': [100, 110]
    }
    api = api_module.API()
    api._get_data = lambda x: pd.DataFrame(data)
    result = api.get_historical('AAPL', interval='1min')
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['date', 'close']
    assert list(result.date) == ['2022-01-01', '2022-01-02']
    assert list(result.close) == [100, 110]

    # Test case when interval is invalid
    with pytest.raises(ValueError):
        api.get_historical('AAPL', interval='invalid')

def test_get_historical_capitalization():
    data = {
        'date': ['2022-01-01', '2022-01-02'],
        'marketCap': [1000000, 1100000]
    }
    api = api_module.API()
    api._get_data = lambda x: pd.DataFrame(data)
    result = api.get_historical_capitalization('AAPL')
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['date', 'marketCap']
    assert list(result.date) == ['2022-01-01', '2022-01-02']
    assert list(result.marketCap) == [1000000, 1100000]