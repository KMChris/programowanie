from api import API

api = API()
data = api.get_historical_price('AAPL')

# Simple Moving Average
def SMA(data, n):
    data = data[:n]['close'].sum()
    return data/n

print(SMA(data, 10))

# Exponential Moving Average
def EMA(data, n):
    data = data[:n]['close']
    ema = data.ewm(com=0.4).mean()
    return ema[0]

print(EMA(data, 10))

import pandas as pd


def stochastic_oscillator(data, n=14):
    """
    Calculates the stochastic oscillator for the given data.
    :param data: pandas DataFrame of historical data with the column 'close'
    :param n: The number of periods for the %K line.
    :return: A tuple of two lists, %K and %D lines.
    """
    data=data[::-1]

    # Find the highest high and lowest low for the last n periods
    highest_high = data['close'].rolling(n).max()
    lowest_low = data['close'].rolling(n).min()

    # Calculate the %K line
    k = 100 * (data['close'] - lowest_low) / (highest_high - lowest_low)

    # Calculate the %D line
    d = k.rolling(n).mean()

    return k[0], d[0]

k,d = stochastic_oscillator(data)
print(k)
print(d)