from src.core.exceptions.InsufficientFundsException import InsufficientFundsException


class Wallet(object):
    """
        Currencies are defined as integers where the last 2 digits
        always represent the decimals (cents)
    """

    def __init__(self, id: int, player_id: int, balance=1000000):
        self.id = id
        self.player_id = player_id
        self.balance = balance

    def credit(self, amount=0):
        self.balance += amount

    def debit(self, amount=0):
        if (self.balance < amount):
            raise InsufficientFundsException(
                balance=self.balance, amount=amount)

        self.balance -= amount

    def __str__(self):
        return f'$ {self.balance / 100}'
