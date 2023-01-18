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