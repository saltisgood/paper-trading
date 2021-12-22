from datetime import datetime

from paper_trader.utils.price import Price


class PriceTime:
    def __init__(self, price: Price, time: datetime):
        self._time = time
        self._price = price

    @property
    def time(self):
        return self._time

    @property
    def price(self):
        return self._price

    def to_sqlite(self):
        return self.price, self.time

    @staticmethod
    def from_sqlite(values):
        price, time = values
        return PriceTime(Price(price), time)
