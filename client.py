import datetime
import pytz
import requests
import urllib
from .objects import *

class Client(object):

    url: str = "https://api-invest.tinkoff.ru/openapi/"
    token: str

    def __init__(self, iv_token: str):

        self.token = iv_token

    def getAccounts(self) -> list[Account]:

        lv_url = self.url + "user/accounts"

        try:
            ls_response = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token}).json()
        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        lt_accounts: list[Account] = []

        for ls_account in ls_response["payload"]["accounts"]:

            lo_account = Account()

            lo_account.type = ls_account["brokerAccountType"]
            lo_account.id = ls_account["brokerAccountId"]

            lt_accounts.append(lo_account)

        return lt_accounts

    def getPortfolioPositions(self) -> list[Position]:

        lv_url = self.url + "portfolio"

        try:
            ls_response = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token}).json()
        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        lt_positions: list[Position] = []

        for ls_position in ls_response["payload"]["positions"]:

            lo_position = Position()

            lo_position.figi = ls_position["figi"]
            lo_position.ticker = ls_position["ticker"]
            lo_position.name = ls_position["name"]
            lo_position.quantity = ls_position["balance"]
            lo_position.lots = ls_position["lots"]
            lo_position.currency = ls_position["averagePositionPrice"]["currency"]
            lo_position.price = ls_position["averagePositionPrice"]["value"]
            lo_position.profit = ls_position["expectedYield"]["value"]

            lt_positions.append(lo_position)

        return lt_positions

    def getPortfolioCurrencies(self) -> list[Currency]:

        lv_url = self.url + "portfolio/currencies"

        try:
            ls_response = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token}).json()
        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        lt_currencies: list[Currency] = []

        for ls_currency in ls_response["payload"]["currencies"]:

            lo_currency = Currency()

            lo_currency.id = ls_currency["currency"]
            lo_currency.balance = ls_currency["balance"]

            lt_currencies.append(lo_currency)

        return lt_currencies

    def getInstruments(self) -> list[Instrument]:

        lt_instruments: list[Instrument] = []

        lt_instruments += self.getCurrencies()
        lt_instruments += self.getShares()
        lt_instruments += self.getBonds()
        lt_instruments += self.getEtfs()

        return lt_instruments

    def getInstrumentByFigi(self, iv_figi: str) -> Instrument:

        ls_params = {
            "figi": iv_figi
        }

        lv_url = self.url + "/market/search/by-figi?" + urllib.parse.urlencode(ls_params)

        try:
            ls_response = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token}).json()
        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        lo_instrument = Instrument()

        lo_instrument.type = ls_response["payload"]["type"]
        lo_instrument.figi = ls_response["payload"]["figi"]
        lo_instrument.ticker = ls_response["payload"]["ticker"]
        lo_instrument.isin = ls_response["payload"]["isin"]
        lo_instrument.name = ls_response["payload"]["name"]
        lo_instrument.currency = ls_response["payload"]["currency"]
        lo_instrument.lot = ls_response["payload"]["lot"]
        lo_instrument.minPriceIncrement = ls_response["payload"]["minPriceIncrement"]

        return lo_instrument

    def getInstrumentByTicker(self, iv_ticker: str) -> Instrument:

        ls_params = {
            "ticker": iv_ticker
        }

        lv_url = self.url + "/market/search/by-ticker?" + urllib.parse.urlencode(ls_params)

        try:
            ls_response = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token}).json()
        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        lo_instrument = Instrument()

        lo_instrument.type = ls_response["payload"]["instruments"][0]["type"]
        lo_instrument.figi = ls_response["payload"]["instruments"][0]["figi"]
        lo_instrument.ticker = ls_response["payload"]["instruments"][0]["ticker"]
        lo_instrument.isin = ls_response["payload"]["instruments"][0]["isin"]
        lo_instrument.name = ls_response["payload"]["instruments"][0]["name"]
        lo_instrument.currency = ls_response["payload"]["instruments"][0]["currency"]
        lo_instrument.lot = ls_response["payload"]["instruments"][0]["lot"]
        lo_instrument.minPriceIncrement = ls_response["payload"]["instruments"][0]["minPriceIncrement"]

        return lo_instrument

    def getCurrencies(self) -> list[Instrument]:

        lv_url = self.url + "market/currencies"

        try:

            lo_request = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token})

            if lo_request.status_code != requests.codes.ok:
                raise Exception("Status code: " + lo_request.status_code)

            ls_response = lo_request.json()

        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        lt_instruments: list[Instrument] = []

        for ls_instrument in ls_response["payload"]["instruments"]:

            lo_instrument = Instrument()

            lo_instrument.type = ls_instrument["type"]
            lo_instrument.figi = ls_instrument["figi"]
            lo_instrument.ticker = ls_instrument["ticker"]
            lo_instrument.name = ls_instrument["name"]
            lo_instrument.currency = ls_instrument["currency"]
            lo_instrument.lot = ls_instrument["lot"]
            lo_instrument.minPriceIncrement = ls_instrument["minPriceIncrement"]

            lt_instruments.append(lo_instrument)

        return lt_instruments

    def getShares(self) -> list[Instrument]:

        lv_url = self.url + "market/stocks"

        try:

            lo_request = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token})

            if lo_request.status_code != requests.codes.ok:
                raise Exception("Status code: " + lo_request.status_code)

            ls_response = lo_request.json()

        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        lt_instruments: list[Instrument] = []

        for ls_instrument in ls_response["payload"]["instruments"]:

            lo_instrument = Instrument()

            lo_instrument.type = ls_instrument["type"]
            lo_instrument.figi = ls_instrument["figi"]
            lo_instrument.ticker = ls_instrument["ticker"]
            lo_instrument.isin = ls_instrument["isin"]
            lo_instrument.name = ls_instrument["name"]
            lo_instrument.currency = ls_instrument["currency"]
            lo_instrument.lot = ls_instrument["lot"]

            if "minPriceIncrement" in ls_instrument:
                lo_instrument.minPriceIncrement = ls_instrument["minPriceIncrement"]

            lt_instruments.append(lo_instrument)

        return lt_instruments

    def getBonds(self) -> list[Instrument]:

        lv_url = self.url + "market/bonds"

        try:

            lo_request = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token})

            if lo_request.status_code != requests.codes.ok:
                raise Exception("Status code: " + lo_request.status_code)

            ls_response = lo_request.json()

        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        lt_instruments: list[Instrument] = []

        # {"figi":"BBG00T22WKV5","ticker":"SU29013RMFS8","isin":"RU000A101KT1","minPriceIncrement":0.01,
        # "faceValue":1E+3,"lot":1,"currency":"RUB","name":"ОФЗ 29013","type":"Bond"}
        for ls_instrument in ls_response["payload"]["instruments"]:

            lo_instrument = Instrument()

            lo_instrument.type = ls_instrument["type"]
            lo_instrument.figi = ls_instrument["figi"]
            lo_instrument.ticker = ls_instrument["ticker"]
            lo_instrument.isin = ls_instrument["isin"]
            lo_instrument.name = ls_instrument["name"]
            lo_instrument.currency = ls_instrument["currency"]
            lo_instrument.lot = ls_instrument["lot"]

            if "minPriceIncrement" in ls_instrument:
                lo_instrument.minPriceIncrement = ls_instrument["minPriceIncrement"]

            lt_instruments.append(lo_instrument)

        return lt_instruments

    def getEtfs(self) -> list[Instrument]:

        lv_url = self.url + "market/etfs"

        try:

            lo_request = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token})

            if lo_request.status_code != requests.codes.ok:
                raise Exception("Status code: " + lo_request.status_code)

            ls_response = lo_request.json()

        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        lt_instruments: list[Instrument] = []

        # {"figi":"BBG333333333","ticker":"TMOS","isin":"RU000A101X76","minPriceIncrement":0.002,"lot":1,
        # "currency":"RUB","name":"Тинькофф iMOEX","type":"Etf"}
        for ls_instrument in ls_response["payload"]["instruments"]:

            lo_instrument = Instrument()

            lo_instrument.type = ls_instrument["type"]
            lo_instrument.figi = ls_instrument["figi"]
            lo_instrument.ticker = ls_instrument["ticker"]
            lo_instrument.isin = ls_instrument["isin"]
            lo_instrument.name = ls_instrument["name"]
            lo_instrument.currency = ls_instrument["currency"]
            lo_instrument.lot = ls_instrument["lot"]
            lo_instrument.minPriceIncrement = ls_instrument["minPriceIncrement"]

            lt_instruments.append(lo_instrument)

        return lt_instruments

    def getCandles(self, iv_ticker: str, iv_interval: str, iv_days: int = 0, iv_hours: int = 0) -> list[Candle]:

        lo_now = datetime.datetime.now(tz=pytz.timezone("Europe/Moscow"))
        lo_prev = lo_now - datetime.timedelta(days=iv_days, hours=iv_hours)

        lo_from = datetime.datetime(lo_prev.year, lo_prev.month, lo_prev.day, 0, 0, 0, 0, pytz.timezone("Europe/Moscow"))
        lo_to = datetime.datetime(lo_now.year, lo_now.month, lo_now.day, 23, 59, 59, 0, pytz.timezone("Europe/Moscow"))

        ls_params = {
            "figi": self.getInstrumentByTicker(iv_ticker).figi,
            "interval": iv_interval,
            "from": lo_from.isoformat(),
            "to": lo_to.isoformat()
        }

        lv_url = self.url + "market/candles?" + urllib.parse.urlencode(ls_params)

        try:
            ls_response = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token}).json()
        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        lt_candles: list[Candle] = []

        for ls_candle in ls_response["payload"]["candles"]:

            lo_candle = Candle()

            lo_candle.time = ls_candle["time"]
            lo_candle.high = ls_candle["h"]
            lo_candle.open = ls_candle["o"]
            lo_candle.close = ls_candle["c"]
            lo_candle.low = ls_candle["l"]
            lo_candle.volume = ls_candle["v"]

            lo_candle.eval()
            
            lt_candles.append(lo_candle)

        return lt_candles

    def getOperations(self,
            io_from: datetime = datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")) - datetime.timedelta(days=365),
            io_to: datetime = datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")),
            iv_ticker: str = "") -> list[Operation]:

        ls_params = {
            "from": io_from.isoformat(),
            "to": io_to.isoformat()
        }

        if iv_ticker != "":
            ls_params["figi"] = self.getInstrumentByTicker(iv_ticker).figi

        lv_url = self.url + "operations?" + urllib.parse.urlencode(ls_params)

        try:

            lo_request = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token})

            if lo_request.status_code != requests.codes.ok:
                raise Exception("Status code: " + lo_request.status_code)

            ls_response = lo_request.json()

        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        lt_operations: list[Operation] = []

        for ls_operation in ls_response["payload"]["operations"]:

            if ls_operation["operationType"] != "Buy" and \
               ls_operation["operationType"] != "BuyCard" and \
               ls_operation["operationType"] != "Sell" and \
               ls_operation["operationType"] != "Dividend" and \
               ls_operation["operationType"] != "TaxDividend" and \
               ls_operation["operationType"] != "Coupon":
                continue

            if ls_operation["status"] != "Done":
                continue

            if ls_operation["figi"] == "BBG005DXJS36" and \
               ls_operation["currency"] == "RUB":
                ls_operation["figi"] = "BBG00QPYJ5H0"

            lo_operation = Operation()

            lo_operation.id = ls_operation["id"]
            lo_operation.type = ls_operation["operationType"]
            lo_operation.figi = ls_operation["figi"]
            lo_operation.currency = ls_operation["currency"]
            lo_operation.date = ls_operation["date"]

            if lo_operation.type == "BuyCard":
                lo_operation.type = "Buy"

            lo_operation.value = abs(ls_operation["payment"])

            if "quantityExecuted" in ls_operation:
                lo_operation.quantity = ls_operation["quantityExecuted"]

            if "price" in ls_operation:
                lo_operation.price = abs(ls_operation["price"])

            if "commission" in ls_operation:
                lo_operation.commission = abs(ls_operation["commission"]["value"])

            lt_operations.insert(0, lo_operation)

        return lt_operations

    def getOrders(self) -> list[Order]:

        lv_url = self.url + "orders"

        try:
            ls_response = requests.get(lv_url, headers={"Authorization": "Bearer " + self.token}).json()
        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        lt_orders: list[Order] = []

        for ls_order in ls_response["payload"]:

            lo_order = Order()

            lo_order.id = ls_order["orderId"]
            lo_order.figi = ls_order["figi"]
            lo_order.type = ls_order["type"]
            lo_order.operation = ls_order["operation"]
            lo_order.status = ls_order["status"]
            lo_order.price = ls_order["price"]
            lo_order.requestedLots = ls_order["requestedLots"]
            lo_order.executedLots = ls_order["executedLots"]

            lt_orders.append(lo_order)

        return lt_orders

    def createLimitOrder(self, iv_ticker: str, iv_operation: str, iv_lots: int, iv_price: float, iv_account_id: str = ""):

        ls_params = {
            "figi": self.getInstrumentByTicker(iv_ticker).figi
        }

        if iv_account_id != "":
            ls_params["brokerAccountId"] = iv_account_id

        ls_data = {
            "lots": iv_lots,
            "operation": iv_operation,
            "price": iv_price,
        }

        lv_url = self.url + "orders/limit-order?" + urllib.parse.urlencode(ls_params)

        try:
            lo_response = requests.post(lv_url, headers={"Authorization": "Bearer " + self.token}, json=ls_data)
        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        ls_response = lo_response.json()

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        return ls_response["payload"]["orderId"]

    def createMarketOrder(self, iv_ticker: str, iv_operation: str, iv_lots: int):

        ls_params = {
            "figi": self.getInstrumentByTicker(iv_ticker).figi
        }

        ls_data = {
            "operation": iv_operation,
            "lots": iv_lots
        }

        lv_url = self.url + "/orders/market-order?" + urllib.parse.urlencode(ls_params)

        try:
            ls_response = requests.post(lv_url, headers={"Authorization": "Bearer " + self.token}, json=ls_data).json()
        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        return ls_response["payload"]["orderId"]

    def cancelOrder(self, iv_id: str):

        ls_params = {
            "orderId": iv_id
        }

        lv_url = self.url + "/orders/cancel?" + urllib.parse.urlencode(ls_params)

        try:
            ls_response = requests.post(lv_url, headers={"Authorization": "Bearer " + self.token}).json()
        except Exception as lx_exception:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lv_url, text=str(lx_exception)))

        if ls_response["status"] == "Error":
            raise Exception(ls_response["payload"]["message"])

        return True
