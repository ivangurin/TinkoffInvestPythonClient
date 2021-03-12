import datetime


class Instrument(object):
    Text: str
    Type: str
    Ticker: str
    FIGI: str
    ISIN: str
    Currency: str
    Lot: int
    MinPriceIncrement: float


class Candle(object):
    Time: str
    High: float
    Open: float
    Close: float
    Low: float
    Volume: float
    ShadowHigh: float
    ShadowLow: float
    Body: float
    Type: str


class Account(object):
    ID: str
    Text: str


class Position(object):
    FIGI: str
    Ticker: str
    Text: str
    Quantity: float
    Lots: int
    Currency: str
    Price: float
    Profit: float


class Order(object):
    typeLimit = "limit"
    typeMarket = "market"

    ID: str
    FIGI: float
    Type: str
    Operation: str
    Price: float
    Status: str
    RequestedLots: int
    ExecutedLots: int


class Operation(object):
    ID: str
    Type: str
    FIGI: str
    Quantity: float
    Price: float
    Value: float
    Commission: float
    Currency: str
    Date: datetime


class Interval(object):
    Min1 = "1min"
    Min2 = "2min"
    Min3 = "3min"
    Min5 = "5min"
    Min10 = "10min"
    Min15 = "15min"
    Min30 = "30min"
    Hour = "hour"
    Day = "day"
    Week = "week"
    Month = "month"
