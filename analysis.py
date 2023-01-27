import pandas as pd
from api import API


class Analysis:

    def __init__(self, symbol, interval='day'):
        self.api = API()
        self.symbol = symbol
        self.data = self.api.get_historical(symbol, interval)
        self.signal = self.get_signal()

    def get_signal(self) -> str:
        """
        Get signal for trading based on technical
        indicators. It is based on the following
        rules:
        - Buy when MACD crosses above signal line
        - Sell when MACD crosses below signal line
        - Buy when RSI is below 30
        - Sell when RSI is above 70
        - Buy when stochastic %K crosses above %D
        - Sell when stochastic %K crosses below %D
        - Buy when SMA is above EMA
        - Sell when SMA is below EMA
        - Buy when SMA is above price
        - Sell when SMA is below price
        - Buy when EMA is above price
        - Sell when EMA is below price

        Returns
        -------
        str
            Signal for trading
        """
        sma = self.sma()
        ema = self.ema()
        rsi = self.rsi()
        macd = self.macd()
        stoch = self.stochastic()
        total_signal = 0
        if macd['MACD'].iloc[-1] > macd['Signal'].iloc[-1]:
            total_signal += 1
        else:
            total_signal -= 1
        if rsi.iloc[-1] < 30:
            total_signal += 1
        elif rsi.iloc[-1] > 70:
            total_signal -= 1
        if stoch['%K'].iloc[-1] > stoch['%D'].iloc[-1]:
            total_signal += 1
        else:
            total_signal -= 1
        if sma.iloc[-1] > ema.iloc[-1]:
            total_signal += 1
        else:
            total_signal -= 1
        if sma.iloc[-1] > self.data['close'].iloc[-1]:
            total_signal += 1
        else:
            total_signal -= 1
        if ema.iloc[-1] > self.data['close'].iloc[-1]:
            total_signal += 1
        else:
            total_signal -= 1
        if total_signal > 1:
            return 'buy'
        elif total_signal < -1:
            return 'sell'
        else:
            return 'neutral'

    def sma(self, period: int = 10) -> pd.DataFrame:
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
        return self.data['close'].rolling(period).mean()

    def ema(self, period: int = 10) -> pd.DataFrame:
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

    def bollinger(self, period: int = 20, std: int = 2) -> pd.DataFrame:
        """
        Bollinger Bands are volatility bands placed above
        and below a moving average. Volatility is based on
        the standard deviation, which changes as volatility
        increases and decreases. The bands automatically
        widen when volatility increases and narrow when
        volatility decreases.

        Parameters
        ----------
        period : int
            Number of periods to calculate Bollinger Bands
        std : int
            Number of standard deviations

        Returns
        -------
        pandas.DataFrame
            Dataframe with Bollinger Bands
        """
        sma = self.sma(period)
        std_dev = self.data['close'].rolling(period).std()
        upper = sma + (std_dev * std)
        lower = sma - (std_dev * std)
        return pd.DataFrame({
            'upper': upper,
            'middle': sma,
            'lower': lower
        })

    def rsi(self, period: int = 14) -> pd.DataFrame:
        """
        Relative Strength Index (RSI) is a momentum
        indicator that measures the magnitude of recent
        price changes to evaluate overbought or
        oversold conditions in the price of a stock
        or other asset.

        Parameters
        ----------
        period : int
            Number of periods to calculate RSI

        Returns
        -------
        pandas.DataFrame
            Dataframe with RSI
        """
        delta = self.data['close'].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        roll_up = up.rolling(period).mean()
        roll_down = down.abs().rolling(period).mean()
        rs = roll_up / roll_down
        return 100 - (100 / (1 + rs))

    def macd(self, signal_period: int = 9, fast_period: int = 12,
             slow_period: int = 26) -> pd.DataFrame:
        """
        Moving Average Convergence Divergence (MACD)
        is a trend-following momentum indicator that
        shows the relationship between two moving
        averages of prices.

        Parameters
        ----------
        signal_period : int
            Number of periods for signal EMA
        slow_period : int
            Number of periods for slow EMA
        fast_period : int
            Number of periods for fast EMA

        Returns
        -------
        pandas.DataFrame
            Dataframe with MACD
        """
        diff = self.ema(fast_period) - self.ema(slow_period)
        signal = diff.ewm(span=signal_period, adjust=False).mean()
        hist = diff - signal
        return pd.DataFrame({
            'MACD': diff,
            'Signal': signal,
            'Histogram': hist
        })


    def stochastic(self, period_k: int = 14, period_d: int = 3,
                   period_s: int = 3) -> pd.DataFrame:
        """
        Stochastic Oscillator is a momentum indicator
        comparing a particular closing price to a range
        of its prices over a certain period of time.

        Parameters
        ----------
        period_k : int
            Number of periods to calculate %K
        period_d : int
            Number of periods to calculate %D
        period_s : int
            Number of periods to calculate SMA

        Returns
        -------
        pandas.DataFrame
            Dataframe with stochastic
        """
        high = self.data['high'].rolling(period_k).max()
        low = self.data['low'].rolling(period_k).min()
        k = 100 * (self.data['close'] - low) / (high - low)
        d = k.rolling(period_d).mean()
        return pd.DataFrame({
            '%K': k,
            '%D': d.rolling(period_s).mean()
        })

    def williams(self, period: int = 14) -> pd.DataFrame:
        """
        Williams %R is a momentum indicator that is the
        inverse of the Fast Stochastic Oscillator. Also
        referred to as %R, Williams %R reflects the level
        of the close relative to the highest high for the
        look-back period.

        Parameters
        ----------
        period : int
            Number of periods to calculate Williams %R

        Returns
        -------
        pandas.DataFrame
            Dataframe with Williams %R
        """
        high = self.data['high']
        low = self.data['low']
        close = self.data['close']
        highest_high = high.rolling(period).max()
        lowest_low = low.rolling(period).min()
        return 100 * (highest_high - close) / (highest_high - lowest_low)


    # TODO Add more indicators:
    # Money Flow Index and Ratio
    # Chaikin Oscillator
    # Accumulation/Distribution
    # True Strength Index
    # KST Oscillator
    # Vortex Indicator: http://www.vortexindicator.com/VFX_VORTEX.PDF
    # Mass Index
    # Trix
    # Standard Deviation
    # Donchian Channel
    # Ultimate Oscillator
    # Keltner Channel
    # Coppock Curve
    # Ease of Movement
    # Force Index
    # On Balance Volume
    # Commodity Channel Index
    # Average Directional Index
    # Bollinger Bands
    # Parabolic SAR
    # Ichimoku Cloud
    # Chande Momentum Oscillator
    # Detrended Price Oscillator
    # Elder-Ray Index
    # Rate of Change
    # Stochastic RSI
    # Williams %R
    # Awesome Oscillator
    # KAMA
    # Hull Moving Average
    # Volume-price Trend
    # Volume-weighted Moving Average
    # Volume Oscillator


if __name__ == "__main__":
    print("This is a module with technical indicators for financial data.")
    analysis = Analysis('AAPL')
    print(analysis.sma(10))
    print(analysis.ema(10))
    print(analysis.rsi(-1))
