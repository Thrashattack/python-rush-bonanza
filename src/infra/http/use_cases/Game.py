from copy import deepcopy
import functools
import json
import operator
from src.core.models.Slots import Slots
from src.core.models.Symbol import Symbol
from src.core.models.Wallet import Wallet
from src.infra.db.TransactionRepository import TransactionRepository
from src.infra.db.WalletRepository import WalletRepository


class Game(object):

    def __init__(self, wallet: Wallet, bet_value: int):
          self.wallet = wallet
          self.bet_value = bet_value
          self.slots = Slots(
            odds=functools.reduce(operator.iconcat, [
              [Symbol(value=100, symbol='../images/mylon.webp')]    * 1,            # 3.50%  1/28
              [Symbol(value=75, symbol='../images/jime.webp')]      * 2,            # 7.14%  2/28
              [Symbol(value=50, symbol='../images/esa.webp')]       * 3,            # 10.71% 3/28
              [Symbol(value=70, symbol='../images/ranger.webp')]    * 4,            # 14.28% 4/28
              [Symbol(value=10, symbol='../images/brucer.webp')]    * 5,            # 17.85% 5/28
              [Symbol(value=25, symbol='../images/minerva.webp')]   * 6,            # 21.42% 6/28
              [Symbol(value=20, symbol='../images/bagre.jpeg')]     * 7,            # 25%    7/28
            ], []),
            scatter=Symbol(value=1, symbol='../images/baiano.webp'))
          self.prize = 0
          self.total_win = 0
          self.updates = []

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
      self.updates.append({ 'action': 'fill_table', 'data': deepcopy(self.slots.table) })
      
      self.slots.find_clusters_and_update()
      self.updates.append({ 'action': 'find_clusters_and_update', 'data': deepcopy(self.slots.table) })
      
      
      while len(self.slots.wins) > 0:
          for win in self.slots.wins:
              amount = (win.prize() // 100) * (self.bet_value // 100) / 100
              self.prize += (win.prize() // 100) * (self.bet_value // 100)
              self.updates.append({ 'action': 'win_symbol', 'data': { 'size': win.size, 'symbol': win.symbol, 'amount': amount } })
              
          self.slots.wins = []
          self.slots.visited = []

          self.slots.tumble_table()
          self.updates.append({ 'action': 'tumble_table', 'data': deepcopy(self.slots.table) })
          
          self.slots.fill_table(only_empty=True)
          self.updates.append({ 'action': 'fill_table', 'data': deepcopy(self.slots.table) })
          
          self.slots.find_clusters_and_update()
          self.updates.append({ 'action': 'find_clusters_and_update', 'data': deepcopy(self.slots.table) })

      if self.prize > 0:
          self.total_win += self.prize
          self.wallet.credit(amount=(self.prize))
          WalletRepository.update_balance(
              balance=self.wallet.balance, wallet_id=self.wallet.id)
          TransactionRepository.create_transaction(
              wallet_id=self.wallet.id, value=self.prize, operation='credit')
          self.updates.append({ 'action': 'prize', 'data': self.total_win / 100})
          
      bonus_rounds = self.slots.bonus_game()
      if bonus_rounds:
          self.updates.append({ 'action': 'bonus_rounds', 'data': bonus_rounds })
          for i in range(bonus_rounds):
              self.updates.append({ 'action': 'round_n', 'data': i + 1})
              self.slots.scatter_count = 0
              self.prize = 0
              self.play(bonus=True)

      if not bonus:
          self.updates.append({ 'action': 'cash_in', 'data': self.total_win })
