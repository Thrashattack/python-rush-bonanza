from src.core.models.Slots import Slots
from src.core.models.Wallet import Wallet
from src.infra.db.WalletRepository import WalletRepository
from src.infra.db.TransactionRepository import TransactionRepository

class Game(object):
    
    
    def __init__(self, wallet: Wallet, bet_value: int):
        self.wallet = wallet
        self.bet_value = bet_value
        self.slots = Slots()
        self.prize = 0
        self.total_win = 0
        

    def play(self, bonus: bool = False):
        if not bonus:
            self.wallet.debit(amount=self.bet_value)
            WalletRepository.update_balance(
                balance=self.wallet.balance, wallet_id=self.wallet.id)
            TransactionRepository.create_transaction(
                wallet_id=self.wallet.id,
                value=self.bet_value,
                operation='debit'
            )

        self.slots.visited = []
        self.slots.wins = []

        self.slots.fill_table()
        yield { 'action': 'fill_table', 'data': self.slots.table }
        
        self.slots.find_clusters_and_update()
        yield { 'action': 'find_clusters_and_update', 'data': self.slots.table }

        while len(self.slots.wins) > 0:
            for win in self.slots.wins:
                amount = (win.prize() // 100) * (self.bet_value // 100) / 100
                self.prize += (win.prize() // 100) * (self.bet_value // 100)
                yield { 'action': 'win_symbol', 'data': { 'size': win.size, 'symbol': win.symbol, 'amount': amount } }
                
            self.slots.wins = []
            self.slots.visited = []

            self.slots.tumble_table()
            yield { 'action': 'tumble_table', 'data': self.slots.table }
            
            self.slots.fill_table(only_empty=True)
            yield { 'action': 'fill_table', 'data': self.slots.table }
            
            self.slots.find_clusters_and_update()
            yield { 'action': 'find_clusters_and_update', 'data': self.slots.table }

        if self.prize > 0:
            self.total_win += self.prize
            self.wallet.credit(amount=(self.prize))
            WalletRepository.update_balance(
                balance=self.wallet.balance, wallet_id=self.wallet.id)
            TransactionRepository.create_transaction(
                wallet_id=self.wallet.id, value=self.prize, operation='credit')
            yield { 'action': 'prize', 'data': self.total_win / 100}
            
        bonus_rounds = self.slots.bonus_game()
        if bonus_rounds:
            yield { 'action': 'bonus_rounds', 'data': bonus_rounds }
            for i in range(bonus_rounds):
                yield { 'action': 'round_n', 'data': i + 1}
                
                self.slots.scatter_count = 0
                self.prize = 0
                for rounds in self.play(bonus=True):
                    yield rounds

        if not bonus:
            yield { 'action': 'cash_in', 'data': self.total_win }