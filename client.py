import pytz
import requests
import urllib
from .objects import *


class Client(object):
    mvUrl: str = "https://api-invest.tinkoff.ru/openapi/"
    mvToken: str

    def __init__(self, ivToken: str):

        self.mvToken = ivToken

    def getCurrencies(self) -> list[Instrument]:

        return self.__getInstruments("currencies")

    def getShares(self) -> list[Instrument]:

        return self.__getInstruments("stocks")

    def getBonds(self) -> list[Instrument]:

        return self.__getInstruments("bonds")

    def getETFs(self) -> list[Instrument]:

        return self.__getInstruments("etfs")

    def getInstrumentByTicker(self, ivTicker: str) -> Instrument:

        lsParams = {
            "ticker": ivTicker
        }

        lsResponse = self.__httpRequest(ivMethod="GET", ivPath="market/search/by-ticker", isParams=lsParams)

        lsInstrument = Instrument()

        lsInstrument.Text = lsResponse["payload"]["instruments"][0]["name"]
        lsInstrument.Type = lsResponse["payload"]["instruments"][0]["type"]
        lsInstrument.FIGI = lsResponse["payload"]["instruments"][0]["figi"]
        lsInstrument.Ticker = lsResponse["payload"]["instruments"][0]["ticker"]
        lsInstrument.ISIN = lsResponse["payload"]["instruments"][0]["isin"]
        lsInstrument.Currency = lsResponse["payload"]["instruments"][0]["currency"]
        lsInstrument.Lot = lsResponse["payload"]["instruments"][0]["lot"]
        lsInstrument.MinPriceIncrement = lsResponse["payload"]["instruments"][0]["minPriceIncrement"]

        return lsInstrument

    def getInstrumentByFIGI(self, ivFIGI: str) -> Instrument:

        lsParams = {
            "figi": ivFIGI
        }

        lsResponse = self.__httpRequest(ivMethod="GET", ivPath="market/search/by-figi", isParams=lsParams)

        lsInstrument = Instrument()

        lsInstrument.Text = lsResponse["payload"]["name"]
        lsInstrument.Type = lsResponse["payload"]["type"]
        lsInstrument.FIGI = lsResponse["payload"]["figi"]
        lsInstrument.Ticker = lsResponse["payload"]["ticker"]
        lsInstrument.ISIN = lsResponse["payload"]["isin"]
        lsInstrument.Currency = lsResponse["payload"]["currency"]
        lsInstrument.Lot = lsResponse["payload"]["lot"]
        lsInstrument.MinPriceIncrement = lsResponse["payload"]["minPriceIncrement"]

        return lsInstrument

    def getCandles(self, ivTicker: str, ivInterval: str, ioFrom: datetime,
                   ioTo: datetime = datetime.datetime.now(tz=pytz.timezone("Europe/Moscow"))) -> list[Candle]:

        lsParams = {
            "figi": self.getInstrumentByTicker(ivTicker).FIGI,
            "interval": ivInterval,
            "from": ioFrom.isoformat(),
            "to": ioTo.isoformat()
        }

        lsResponse = self.__httpRequest(ivMethod="GET", ivPath="market/candles", isParams=lsParams)

        ltCandles: list[Candle] = []

        for lsResponseCandle in lsResponse["payload"]["candles"]:
            lsCandle = Candle()

            lsCandle.Time = lsResponseCandle["time"]
            lsCandle.High = lsResponseCandle["h"]
            lsCandle.Open = lsResponseCandle["o"]
            lsCandle.Close = lsResponseCandle["c"]
            lsCandle.Low = lsResponseCandle["l"]
            lsCandle.Volume = lsResponseCandle["v"]

            if lsCandle.Open < lsCandle.Close:
                lsCandle.Type = "green"
                lsCandle.ShadowHigh = lsCandle.High - lsCandle.Close
                lsCandle.Body = lsCandle.Close - lsCandle.Open
                lsCandle.ShadowLow = lsCandle.Open - lsCandle.Low
            else:
                lsCandle.Type = "red"
                lsCandle.ShadowHigh = lsCandle.High - lsCandle.Open
                lsCandle.Body = lsCandle.Open - lsCandle.Close
                lsCandle.ShadowLow = lsCandle.Close - lsCandle.Low

            ltCandles.append(lsCandle)

        return ltCandles

    def getAccounts(self) -> list[Account]:

        lsResponse = self.__httpRequest(ivMethod="GET", ivPath="user/accounts")

        if lsResponse["status"] == "Error":
            raise Exception(lsResponse["payload"]["message"])

        ltAccounts: list[Account] = []

        for lsAccount in lsResponse["payload"]["accounts"]:
            lsAccount = Account()

            lsAccount.ID = lsAccount["brokerAccountId"]
            lsAccount.Text = lsAccount["brokerAccountType"]

            ltAccounts.append(lsAccount)

        return ltAccounts

    def getPositions(self) -> list[Position]:

        lsResponse = self.__httpRequest(ivMethod="GET", ivPath="portfolio")

        if lsResponse["status"] == "Error":
            raise Exception(lsResponse["payload"]["message"])

        ltPositions: list[Position] = []

        for lsResponsePosition in lsResponse["payload"]["positions"]:
            lsPosition = Position()

            lsPosition.FIGI = lsResponsePosition["figi"]
            lsPosition.Ticker = lsResponsePosition["ticker"]
            lsPosition.Text = lsResponsePosition["name"]
            lsPosition.Quantity = lsResponsePosition["balance"]
            lsPosition.Lots = lsResponsePosition["lots"]
            lsPosition.Currency = lsResponsePosition["averagePositionPrice"]["currency"]
            lsPosition.Price = lsResponsePosition["averagePositionPrice"]["value"]
            lsPosition.Profit = lsResponsePosition["expectedYield"]["value"]

            ltPositions.append(lsPosition)

        return ltPositions

    def getOperations(self, ivTicker: str, ioFrom: datetime,
                      ioTo: datetime = datetime.datetime.now(tz=pytz.timezone("Europe/Moscow"))) -> list[
        Operation]:

        lsParams = {
            "from": ioFrom.isoformat(),
            "to": ioTo.isoformat()
        }

        if ivTicker != "":
            lsParams["figi"] = self.getInstrumentByTicker(ivTicker).FIGI

        lsResponse = self.__httpRequest(ivMethod="GET", ivPath="operations", isParams=lsParams)

        ltOperations: list[Operation] = []

        for lsResponseOperation in lsResponse["payload"]["operations"]:

            if lsResponseOperation["operationType"] != "Buy" and \
                    lsResponseOperation["operationType"] != "BuyCard" and \
                    lsResponseOperation["operationType"] != "Sell" and \
                    lsResponseOperation["operationType"] != "Dividend" and \
                    lsResponseOperation["operationType"] != "TaxDividend" and \
                    lsResponseOperation["operationType"] != "Coupon" and \
                    lsResponseOperation["operationType"] != "TaxCoupon":
                continue

            if lsResponseOperation["status"] != "Done":
                continue

            if lsResponseOperation["operationType"] == "BuyCard":
                lsResponseOperation["operationType"] = "Buy"

            lsOperation = Operation()

            lsOperation.ID = lsResponseOperation["id"]
            lsOperation.Type = lsResponseOperation["operationType"]
            lsOperation.FIGI = lsResponseOperation["figi"]
            lsOperation.Currency = lsResponseOperation["currency"]
            lsOperation.Date = lsResponseOperation["date"]
            lsOperation.Value = abs(lsResponseOperation["payment"])

            if "quantityExecuted" in lsResponseOperation:
                lsOperation.Quantity = lsResponseOperation["quantityExecuted"]

            if "price" in lsResponseOperation:
                lsOperation.Price = abs(lsResponseOperation["price"])

            if "commission" in lsResponseOperation:
                lsOperation.Commission = abs(lsResponseOperation["commission"]["value"])

            ltOperations.insert(0, lsOperation)

        return ltOperations

    def getOrders(self) -> list[Order]:

        lsResponse = self.__httpRequest(ivMethod="GET", ivPath="orders")

        ltOrders: list[Order] = []

        for lsResponseOrder in lsResponse["payload"]:
            lsOrder = Order()

            lsOrder.ID = lsResponseOrder["orderId"]
            lsOrder.FIGI = lsResponseOrder["figi"]
            lsOrder.Type = lsResponseOrder["type"]
            lsOrder.Operation = lsResponseOrder["operation"]
            lsOrder.Status = lsResponseOrder["status"]
            lsOrder.Price = lsResponseOrder["price"]
            lsOrder.RequestedLots = lsResponseOrder["requestedLots"]
            lsOrder.ExecutedLotsxecutedLots = lsResponseOrder["executedLots"]

            ltOrders.append(lsOrder)

        return ltOrders

    def createLimitOrder(self, ivTicker: str, ivOperation: str, ivLots: int, ivPrice: float):

        return self.__createOrder(ivType=Order.typeLimit, ivTicker=ivTicker, ivOperation=ivOperation,
                                  ivLots=ivLots,
                                  ivPrice=ivPrice)

    def createMarketOrder(self, ivTicker: str, ivOperation: str, ivLots: int):

        return self.__createOrder(ivType=Order.typeMarket, ivTicker=ivTicker, ivOperation=ivOperation,
                                  ivLots=ivLots)

    def cancelOrder(self, ivOrderID: str):

        lsParams = {
            "orderId": ivOrderID
        }

        self.__httpRequest(ivMethod="POST", ivPath="orders/cancel", isParams=lsParams)

        return True

    def __getInstruments(self, ivType: str) -> list[Instrument]:

        lsResponse = self.__httpRequest(ivMethod="GET", ivPath="market/" + ivType)

        ltInstruments: list[Instrument] = []

        for lsResponseInstrument in lsResponse["payload"]["instruments"]:

            lsInstrument = Instrument()

            lsInstrument.Text = lsResponseInstrument["name"]
            lsInstrument.Type = lsResponseInstrument["type"]
            lsInstrument.FIGI = lsResponseInstrument["figi"]
            lsInstrument.Ticker = lsResponseInstrument["ticker"]

            if "isin" in lsResponseInstrument:
                lsInstrument.ISIN = lsResponseInstrument["isin"]

            lsInstrument.Currency = lsResponseInstrument["currency"]
            lsInstrument.Lot = lsResponseInstrument["lot"]

            if "minPriceIncrement" in lsResponseInstrument:
                lsInstrument.MinPriceIncrement = lsResponseInstrument["minPriceIncrement"]

            ltInstruments.append(lsInstrument)

        return ltInstruments

    def __createOrder(self, ivType: str, ivTicker: str, ivOperation: str, ivLots: int, ivPrice: float = 0) -> str:

        lsParams = {
            "figi": self.getInstrumentByTicker(ivTicker).FIGI
        }

        lsData = {
            "operation": ivOperation,
            "lots": ivLots,
            "price": ivPrice,
        }

        lsResponse = self.__httpRequest(ivMethod="POST", ivPath="orders/" + ivType + "-order", isParams=lsParams,
                                        isData=lsData)

        return lsResponse["payload"]["orderId"]

    def __httpRequest(self, ivMethod: str, ivPath: str, isParams={}, isData={}) -> str:

        lvUrl = self.mvUrl + ivPath + "?" + urllib.parse.urlencode(isParams)

        lsHeader = {
            "Authorization": "Bearer " + self.mvToken
        }

        try:

            if ivMethod == "GET":

                loRequest = requests.get(lvUrl, headers=lsHeader)

            elif ivMethod == "POST":

                loRequest = requests.post(lvUrl, headers=lsHeader, json=isData)

        except Exception as loException:
            raise Exception('Failed to get data from {url}: {text}'.format(url=lvUrl, text=str(loException)))

        if loRequest.status_code != requests.codes.ok:
            raise Exception("HTTP returns code: " + str(loRequest.status_code))

        lsResponse = loRequest.json()

        if lsResponse["status"] == "Error":
            raise Exception(lsResponse["payload"]["message"])

        return lsResponse
