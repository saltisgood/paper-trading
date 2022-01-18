from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from statistics import median

from paper_trader.exchange.history import PriceTimes, SymbolPriceTime
from paper_trader.exchange.orders import Fill, Side
from paper_trader.exchange.position import Position
from paper_trader.statistics import mean
from paper_trader.utils.price import Price

from .simulator import Simulation


@dataclass
class _CloseDiff:
    absolute_diff: Price
    percent_diff: Price


_CloseDiffs = list[_CloseDiff]


@dataclass
class DailyTrend:
    ave_diff: Price = Price(Decimal("0.0"))
    ave_diff_pct: Decimal = Decimal("0.0")

    median_diff: Price = Price(Decimal("0.0"))
    median_diff_pct: Decimal = Decimal("0.0")

    positive_days: int = 0
    total_days: int = 0

    @staticmethod
    def _from_data(data: _CloseDiffs):
        if not data:
            return None

        return DailyTrend(
            Price(mean(d.absolute_diff.value for d in data)),
            mean(d.percent_diff for d in data),
            Price(median(d.absolute_diff.value for d in data)),
            median(d.percent_diff for d in data),
            sum(1 for d in data if d.absolute_diff.value > 0),
            len(data),
        )

    def __str__(self):
        return f'Ave change: ${self.ave_diff}, ({(self.ave_diff_pct * Decimal("100.0")).quantize(Decimal("1.000"))}%), Median: ${self.median_diff}, ({(self.median_diff_pct * Decimal("100.0")).quantize(Decimal("1.000"))}%), Positive Days: {self.positive_days}/{self.total_days}'


class DowIndexMixin:
    """
    DOW = Day of week
    """

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)
        assert isinstance(index, int)
        dow_indexing = {0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri"}
        return self[dow_indexing[index]]


@dataclass
class _WeeklyCloseDiffs(DowIndexMixin):
    mon: _CloseDiffs = field(default_factory=_CloseDiffs)
    tue: _CloseDiffs = field(default_factory=_CloseDiffs)
    wed: _CloseDiffs = field(default_factory=_CloseDiffs)
    thu: _CloseDiffs = field(default_factory=_CloseDiffs)
    fri: _CloseDiffs = field(default_factory=_CloseDiffs)


@dataclass
class WeeklyTrend(DowIndexMixin):
    mon: DailyTrend = DailyTrend()
    tue: DailyTrend = DailyTrend()
    wed: DailyTrend = DailyTrend()
    thu: DailyTrend = DailyTrend()
    fri: DailyTrend = DailyTrend()

    @property
    def days(self):
        return [self.mon, self.tue, self.wed, self.thu, self.fri]

    @staticmethod
    def _from_data(data: _WeeklyCloseDiffs):
        return WeeklyTrend(*(DailyTrend._from_data(data[x]) for x in range(5)))

    def __str__(self):
        return f"Mon: {self.mon},\nTue: {self.tue},\nWed: {self.wed},\nThu: {self.thu},\nFri: {self.fri}"


def weekly_trend(close_prices: PriceTimes):
    """
    close_prices assumed to be sorted by time
    """

    dow_diffs = _WeeklyCloseDiffs()

    for prev_close, this_close in zip(close_prices[:-1], close_prices[1:]):
        diff_abs = this_close.price - prev_close.price
        diff_pct = (
            diff_abs / prev_close.price
        )  # TODO: Check if this is right or if it's over close_price

        dow_diff = dow_diffs[this_close.time.weekday()]
        dow_diff.append(_CloseDiff(diff_abs, diff_pct))

    return WeeklyTrend._from_data(dow_diffs)


class DowSimulator:
    def __init__(self, sim: Simulation, starting_cash: Price):
        self._sim = sim
        self._starting_cash = starting_cash
        self._cash = starting_cash
        self._fee = Price("5.00")
        self._start_date: datetime = None
        self._end_date: datetime = None
        self._actions = {0: Side.BUY, 1: Side.SELL, 2: Side.BUY, 3: Side.SELL}

    def on_begin(self):
        pass

    def on_end(self):
        print(f"From {self._start_date} to {self._end_date}:")
        print(f"Starting cash: {self._starting_cash}")
        print(f"Final cash: {self._cash}")

        holding_value = Price("0.0")
        for symbol in self._sim.default_book.positions.positions.keys():
            quantity = self._sim.default_book.positions.positions[
                symbol
            ].net_quantity
            if quantity > 0:
                last_price = self._sim.get_last_price(symbol)
                print(f"Holding {quantity} @ {last_price}")
                holding_value += quantity * last_price
        profit = self._cash - self._starting_cash + holding_value
        print(f"Profit: {profit} ({100 * profit / self._starting_cash}%)")

    def on_price(self, price: SymbolPriceTime):
        if self._start_date is None:
            self._start_date = price.time
        self._end_date = price.time
        self._sim.set_last_price(price.symbol, price.price)

        dow = price.time.weekday()
        try:
            action = self._actions[dow]
        except KeyError:
            action = None

        if action == Side.BUY:
            self._buy_max(price)
        elif action == Side.SELL:
            self._sell_max(price)

    def _buy_max(self, price: SymbolPriceTime):
        quantity = int((self._cash - self._fee) / price.price)
        if quantity > 0:
            self._cash -= self._fee + (quantity * price.price)
            self._sim.add_fill(
                Fill(
                    price.symbol,
                    price.time,
                    Side.BUY,
                    price.price,
                    quantity,
                    self._fee,
                )
            )

    def _sell_max(self, price: SymbolPriceTime):
        quantity = self._sim.default_book.positions.positions.get(
            price.symbol, Position()
        ).net_quantity
        if quantity > 0:
            self._cash += (quantity * price.price) - self._fee
            self._sim.add_fill(
                Fill(
                    price.symbol,
                    price.time,
                    Side.SELL,
                    price.price,
                    quantity,
                    self._fee,
                )
            )
