from analysis import Analysis
import pandas as pd
import pytest

# Create a new instance of Analysis class without
# calling __init__ method (which would require API key)
analysis = object.__new__(Analysis)

def test_sma():
    """
    Test simple moving average (SMA)
    """
    analysis.data = pd.DataFrame(
        {'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
    )

    # Test for default values
    sma = analysis.sma()
    assert sma[9] == 5.5
    assert sma[:9].isnull().all()

    # Test for custom values
    sma = analysis.sma(5)
    assert sma[4] == 3.0
    assert sma[:4].isnull().all()

    # Test for ValueError
    with pytest.raises(ValueError):
        analysis.sma(-1)

def test_ema():
    """
    Test exponential moving average (EMA)
    """
    analysis.data = pd.DataFrame(
        {'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
    )

    # Test for default values
    ema = analysis.ema()
    assert pytest.approx(ema[9]) == 6.239368

    # Test for custom values
    ema = analysis.ema(5)
    assert pytest.approx(ema[4]) == 3.395062

    # Test for ValueError
    with pytest.raises(ValueError):
        analysis.ema(0)

def test_bollinger():
    """
    Test Bollinger bands
    """
    analysis.data = pd.DataFrame(
        {'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                   11, 12, 13, 14, 15, 16, 17, 18,
                   19, 20, 21, 22, 23, 24, 25, 26]}
    )

    # Test for default values
    bands = analysis.bollinger()
    assert pytest.approx(bands['upper'].iloc[25]) == 28.332159
    assert pytest.approx(bands['lower'].iloc[25]) == 4.667840
    assert pytest.approx(bands['middle'].iloc[25]) == 16.5

    # Test for custom values
    bands = analysis.bollinger(5, 2)
    assert pytest.approx(bands['upper'].iloc[4]) == 6.162277
    assert pytest.approx(bands['lower'].iloc[4]) == -0.16227766
    assert pytest.approx(bands['middle'].iloc[4]) == 3.0

    # Test for ValueError
    with pytest.raises(ValueError):
        analysis.bollinger(-1)

def test_rsi():
    """
    Test relative strength index (RSI)
    """
    analysis.data = pd.DataFrame(
        {'close': [5, 4, 3, 2, 1, 2, 3, 4,
                   5, 6, 7, 8, 9, 10, 11,
                   12, 13, 14, 15, 16, 17]}
    )

    # Test for default values
    rsi = analysis.rsi()
    values = [71.428571, 78.571429, 85.714286,
              92.857143, 100.0, 100.0, 100.0]
    for i, r in enumerate(rsi[14:]):
        assert pytest.approx(r) == values[i]
    assert rsi[:14].isnull().all()

    # Test for custom values
    rsi = analysis.rsi(5)
    values = [20.0, 40.0, 60.0, 80.0, 100.0, 100.0,
              100.0, 100.0, 100.0, 100.0, 100.0,
              100.0, 100.0, 100.0, 100.0, 100.0]
    for i, r in enumerate(rsi[5:]):
        assert pytest.approx(r) == values[i]
    assert rsi[:5].isnull().all()

    # Test for extreme values
    rsi = analysis.rsi(1)
    assert (rsi[5:] == 100.0).all()
    assert (rsi[1:5] == 0.0).all()
    assert rsi.isnull()[0]
    rsi = analysis.rsi(0)
    assert rsi.isnull().all()

    # Test for ValueError
    with pytest.raises(ValueError):
        analysis.rsi(-1)

def test_macd():
    """
    Test moving average convergence divergence (MACD)
    """
    analysis.data = pd.DataFrame(
        {'close': [ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
                    11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                    21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}
    )

    # Test for default values
    macd = analysis.macd()
    assert pytest.approx(macd['MACD'][29]) == 5.701697
    assert pytest.approx(macd['Signal'][29]) == 5.172207
    assert pytest.approx(macd['Histogram'][29]) == 0.529490

    # Test for custom values
    macd = analysis.macd(5, 10, 15)
    values = [1.777262, 1.855002, 1.925316,
              1.988715, 2.045724, 2.096861,
              2.142633, 2.183523, 2.219990,
              2.252460, 2.281332, 2.306971,
              2.329714, 2.349866, 2.367704]
    for i, m in enumerate(macd['MACD'][15:]):
        assert pytest.approx(m) == values[i]

    # Test for ValueError
    with pytest.raises(ValueError):
        analysis.macd(0, 10, 15)
    with pytest.raises(ValueError):
        analysis.macd(5, 0, 15)
    with pytest.raises(ValueError):
        analysis.macd(5, 10, 0)

def test_stochastic():
    """
    Test stochastic oscillator
    """
    analysis.data = pd.DataFrame(
        {'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                   11, 12, 13, 14, 15, 16, 17, 18],
         'high': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                  12, 13, 14, 15, 16, 17, 18, 19],
         'low': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                 10, 11, 12, 13, 14, 15, 16, 17]}
    )

    # Test for default values
    stoch = analysis.stochastic()
    assert pytest.approx(stoch['%K'].iloc[13]) == 93.333333
    assert pytest.approx(stoch['%D'].iloc[17]) == 93.333333

    # Test for custom values
    stoch = analysis.stochastic(5)
    assert pytest.approx(stoch['%K'].iloc[4]) == 83.333333
    assert pytest.approx(stoch['%D'].iloc[8]) == 83.333333

    # Test for ValueError
    with pytest.raises(ValueError):
        analysis.stochastic(-1)
    with pytest.raises(ValueError):
        analysis.stochastic(14, -1)
    with pytest.raises(ValueError):
        analysis.stochastic(14, 3, -1)

def test_williams():
    """
    Test Williams %R
    """
    analysis.data = pd.DataFrame(
        {'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                   11, 12, 13, 14, 15, 16, 17, 18],
         'high': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                  12, 13, 14, 15, 16, 17, 18, 19],
         'low': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                 10, 11, 12, 13, 14, 15, 16, 17]}
    )

    # Test for default values
    williams = analysis.williams()
    assert pytest.approx(williams.iloc[13]) == 6.666667

    # Test for custom values
    williams = analysis.williams(5)
    assert pytest.approx(williams.iloc[4]) == 16.666667

    # Test for ValueError
    with pytest.raises(ValueError):
        analysis.williams(-1)
