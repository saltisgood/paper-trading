from typing import Dict, List

from .orders import Fill

Fills = List[Fill]


class Position:
    def __init__(self):
        self._fills = Fills()

    @property
    def net_quantity(self):
        return sum(f.net_quantity for f in self._fills)


ItemKey = str
Positions = Dict[ItemKey, Position]


class TotalPositions:
    def __init__(self):
        self._positions = Positions()
