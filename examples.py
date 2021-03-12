import datetime
import objects
import pytz
from client import Client

loClient = Client('TOKEN')

# Shares(similar for Bonds and ETFs)
ltShares = loClient.getShares()

for lsShare in ltShares:
    print(lsShare.__dict__)

# Candles
ltCandles = loClient.getCandles(
    ivTicker="AAPL", ivInterval=objects.Interval.Day,
    ioFrom=datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")) - datetime.timedelta(days=30),
    ioTo=datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")))

for lsCandle in ltCandles:
    print(lsCandle.__dict__)

# Accounts
ltAccounts = loClient.getAccounts()

for lsAccount in ltAccounts:
    print(lsAccount.__dict__)

# Positions
ltPositions = loClient.getPortfolioPositions()

for lsPosition in ltPositions:
    print(lsPosition.__dict__)

# Operations
ltOperations = loClient.getOperations(
    ivTicker="",
    ioFrom=datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")) - datetime.timedelta(days=30))

for lsOperation in ltOperations:
    print(lsOperation.__dict__)

# Create order
lvOrderId = loClient.createLimitOrder(ivTicker="AAPL", ivOperation="Buy", ivLots=1, ivPrice=70)

print(lvOrderId)

# Orders
ltOrders = loClient.getOrders()

for lsOrder in ltOrders:
    print(lsOrder.__dict__)

# Cancel order
loClient.cancelOrder(lvOrderId)
