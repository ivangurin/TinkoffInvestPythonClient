import tinvest

lo_client = tinvest.Client('TOKEN')

# Get accounts
lt_accounts = lo_client.getAccounts()

for lo_account in lt_accounts:
    print(lo_account.__dict__)

# Get portfolio
lt_positions = lo_client.getPortfolioPositions()

for lo_position in lt_positions:
    print(lo_position.__dict__)

# Operations
lt_operations = lo_client.getOperations()

for lo_operation in lt_operations:
    print(lo_operation.__dict__)

# Get instruments
lt_instruments = lo_client.getInstruments()

for lo_instrument in lt_instruments:
    print(lo_instrument.__dict__)

# Get candles
lt_candles = lo_client.getCandles(iv_figi="BBG000B9XRY4", iv_interval=tinvest.Interval.day, iv_days=10)

for lo_candle in lt_candles:
    print(lo_candle.__dict__)

# Create order
lv_orderId = lo_client.createLimitOrder(iv_figi="BBG000B9XRY4", iv_operation="Buy", iv_lots=1, iv_price=65)

print(lv_orderId)

# Get orders
lt_Orders = lo_client.getOrders()

for lo_order in lt_Orders:
    print(lo_order.__dict__)

# Cancel order
lo_client.cancelOrder(lv_orderId)
