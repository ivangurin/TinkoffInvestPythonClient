import datetime


class Account(object):

    type: str
    id: str


class Position(object):

    figi: str
    ticker: str
    name: str
    quantity: int
    lots: int
    currency: str
    price: float
    profit: float


class Currency(object):

    id: str
    balance: float
    blocked: str


class Order(object):

    id: str
    figi: float
    type: str
    operation: str
    price: float
    status: str
    requestedLots: int
    executedLots: int


class Instrument(object):

    type: str
    ticker: str
    figi: str
    isin: str
    name: str
    currency: str
    lot: int
    minPriceIncrement: float


class Operation(object):
    id: str
    type: str
    figi: str
    quantity: int
    price: float
    value: float
    commission: float
    currency: str
    date: datetime

    def __init__(self):
        self.id = ""
        self.type = ""
        self.figi = ""
        self.quantity = ""
        self.currency = ""
        self.price = 0
        self.value = 0
        self.commission = 0

class Candle(object):

    type: str
    open: int
    max: int
    min: int
    close: int
    volume: int
    shadow_high: int
    shadow_low: int
    body: int
    time: str

    def eval(self):

        if self.open < self.close:
            self.type = "green"
            self.shadow_high = self.max - self.close
            self.body = self.close - self.open
            self.shadow_low = self.open - self.min
        else:
            self.type = "red"
            self.shadow_high = self.max - self.open
            self.body = self.open - self.close
            self.shadow_low = self.close - self.min


class Interval(object):

    min1 = "1min"
    min2 = "2min"
    min3 = "3min"
    min5 = "5min"
    min10 = "10min"
    min15 = "15min"
    min30 = "30min"
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"

