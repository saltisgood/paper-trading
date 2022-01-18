from typing import Protocol


class Persistence(Protocol):
    def load_symbols(self):
        raise NotImplementedError()
