import pandas as pd
from api import API


class Analysis:

    def __init__(self, symbol, interval='day'):
        self.api = API()
        self.symbol = symbol
        self.data = self.api.get_historical(symbol, interval)

    def SMA(self, period: int) -> pd.DataFrame:
        """
        Simple Moving Average (SMA) is the most basic
        type of moving average. It is calculated by
        adding the closing price for the last n days
        and dividing the sum by n.

        Parameters
        ----------
        period : int
            Number of periods to calculate SMA

        Returns
        -------
        pandas.DataFrame
            Dataframe with SMA
        """
        return self.data['close'].rolling(
            period).mean()

    def EMA(self, period: int) -> pd.DataFrame:
        """
        Exponential Moving Average (EMA) is a type of
        moving average that places a greater weight and
        significance on the most recent data points.
        The exponential moving average reacts more
        significantly to recent price changes than a
        simple moving average (SMA) which applies an
        equal weight to all observations in the period.

        Parameters
        ----------
        period : int
            Number of periods to calculate EMA

        Returns
        -------
        pandas.DataFrame
            Dataframe with EMA
        """
        return self.data['close'].ewm(
            span=period, adjust=False).mean()

print(SMA(data, 10))

# Exponential Moving Average
def EMA(data, n):
    data = data[:n]['close']
    ema = data.ewm(com=0.4).mean()
    return ema[0]

print(EMA(data, 10))