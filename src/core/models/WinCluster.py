from src.core.models.Symbol import Symbol


class WinCluster(object):
    MIN_TO_WIN = 5
    SIZE_MULTIPLIER = {
        '5': 100,   # x1.00
        '6': 125,   # x1.25
        '7': 150,   # x1.50
        '8': 200,   # x2.00
        '9': 250,   # x2.50
        '10': 500,  # x5.00
        '11': 750,  # x7.50
        '12': 900,  # x9.00
        '13': 1000,  # x10.00
        '14': 1200,  # x12.00
        '15': 1500,  # x15.00
    }

    def __init__(self, symbol: Symbol, size: int, start: list[int]):
        self.symbol = symbol
        self.size = size
        self.start = start

    def prize(self):
        if self.size > 15:
            self.size = 15

        multiplier = self.SIZE_MULTIPLIER[str(self.size)]

        return self.symbol.value * multiplier
