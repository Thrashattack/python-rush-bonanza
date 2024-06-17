class Symbol(dict):
    """
        The value of a symbol represents the percentage of the bet that it pays
        E.g bet = 100 ($1.00)
        symbol.value = 25 (x0.25)
        Pays 25 ($0.25) -> (100 / 100) * 25 = 25
    """

    def __init__(self, value: int, symbol: str):
        self.value = value
        self.symbol = symbol
        dict.__init__(self, symbol=symbol)

    def __str__(self):
        return self.symbol

    def __eq__(self, other: object):
        return self.value == other.value
