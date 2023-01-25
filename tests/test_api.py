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

