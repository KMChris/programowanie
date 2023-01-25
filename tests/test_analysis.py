import pandas as pd
from src.analysis import Analysis

analysis = Analysis('AAPl')


def test_sma():
    analysis.data = pd.DataFrame({'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    analysis.sma(10)
    assert analysis.sma(10)[9] == 5.5