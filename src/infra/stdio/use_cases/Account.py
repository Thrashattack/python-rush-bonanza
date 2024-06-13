from src.infra.db.PlayerRepository import PlayerRepository
from src.infra.db.WalletRepository import WalletRepository
from src.infra.db.TransactionRepository import TransactionRepository


class Account(object):

    SIGNUP_BONUS = 1000000

    def __init__(self, name: str, password):
        self.name = name
        self.password = password
        self.wallet = None
        self.transactions = []

    def signin(self):
        player = PlayerRepository.fetch_player(
            name=self.name, password=self.password)
        self.wallet = WalletRepository.fetch_wallet(player_id=player.id)

    def signup(self):
        player = PlayerRepository.create_player(
            name=self.name, password=self.password)
        self.wallet = WalletRepository.create_wallet(
            player_id=player.id, balance=self.SIGNUP_BONUS)
        TransactionRepository.create_transaction(
            wallet_id=self.wallet.id,
            value=self.SIGNUP_BONUS,
            operation='signup'
        )

    def fetch_transactions(self):
        self.transactions = TransactionRepository.fetch_transactions(
            wallet_id=self.wallet.id, limit=20)

    def calc_rtp(self):
        all_transactions = TransactionRepository.fetch_transactions(
            wallet_id=self.wallet.id, limit=10000)
        data = {
            'debit': 0,
            'credit': 0,
            'balance': 0,
            'transactions': len(all_transactions),
        }

        for transaction in all_transactions:
            value = transaction[1]
            operation = transaction[2]

            if operation == 'signup':
                continue

            data[operation] += value

        data['balance'] = data['credit'] - data['debit']

        return data
