from datetime import datetime, timedelta
from typing import Protocol

from paper_trader.exchange.book import Book
from paper_trader.exchange.history import SymbolPriceTime, SymbolPriceTimes
from paper_trader.exchange.orders import Fill
from paper_trader.exchange.position import Position
from paper_trader.utils.price import Price


class Simulator(Protocol):
    def on_begin(self):
        raise NotImplementedError()

    def on_price(self, price: SymbolPriceTime):
        raise NotImplementedError()

    def on_end(self):
        raise NotImplementedError()


class Simulation:
    def __init__(self):
        BookDict = dict[str, Book]
        self._books = BookDict()
        self._books["default"] = Book("default")
        self._last_prices: dict[str, Price] = {}

    @property
    def default_book(self):
        return self._books["default"]

    def add_fill(self, fill: Fill):
        try:
            pos = self.default_book.positions.positions[fill.symbol]
        except KeyError:
            pos = Position()
            self.default_book.positions.positions[fill.symbol] = pos
        pos.fills.append(fill)

    def get_last_price(self, symbol: str) -> Price | None:
        try:
            return self._last_prices[symbol]
        except KeyError:
            return None

    def set_last_price(self, symbol: str, price: Price):
        self._last_prices[symbol] = price


class Filter(Protocol):
    def is_relevant(self, price: SymbolPriceTime) -> bool:
        raise NotImplementedError()


class NullFilter:
    def is_relevant(self, price: SymbolPriceTime) -> bool:
        return True


class SymbolFilter:
    def __init__(self, symbols: set[str]):
        self._relevant_symbols = symbols

    def is_relevant(self, price: SymbolPriceTime) -> bool:
        return price.symbol in self._relevant_symbols


class AndFilter:
    def __init__(self, filters: list[Filter]):
        self._filters = filters

    def is_relevant(self, price: SymbolPriceTime) -> bool:
        return all(f.is_relevant(price) for f in self._filters)


class OrFilter:
    def __init__(self, filters: list[Filter]):
        self._filters = filters

    def is_relevant(self, price: SymbolPriceTime) -> bool:
        return any(f.is_relevant(price) for f in self._filters)


class DateFilter:
    def __init__(
        self, after_date: datetime = None, back_time: timedelta = None
    ):
        if after_date is not None:
            self._after_date = after_date
        elif back_time is not None:
            self._after_date = datetime.now() - back_time
        else:
            raise Exception("Invalid arguments")

    def is_relevant(self, price: SymbolPriceTime) -> bool:
        return price.time >= self._after_date


def filter(f: Filter):
    class _Filter:
        def __ror__(self, prices: SymbolPriceTimes):
            return SymbolPriceTimes(p for p in prices if f.is_relevant(p))

    return _Filter()


class SimulationRunner:
    def __init__(self, data: SymbolPriceTimes):
        self._data = data

    def run(self, simulator: Simulator, filter: Filter = NullFilter()):
        simulator.on_begin()
        for price in self._data:
            if filter.is_relevant(price):
                simulator.on_price(price)
        simulator.on_end()
