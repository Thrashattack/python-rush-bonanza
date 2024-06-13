class InsufficientFundsException(BaseException):
    def __init__(self, balance: int, amount: int):
        super(InsufficientFundsException, self).__init__(
            f'Trying to withdraw {amount / 100} from {balance / 100}')
