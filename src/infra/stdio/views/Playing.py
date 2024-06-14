import os
import time
import curses

from src.infra.stdio.use_cases.Game import Game
from playsound import playsound

class Playing(object):
    TUMBLING_SOUND = os.path.join(os.path.dirname(
        __file__), '../assets/mixkit-cards-deck-hits-1994.wav')
    GAME_OVER_SOUND = os.path.join(os.path.dirname(
        __file__), '../assets/mixkit-casino-bling-achievement-2067.wav')
    TOTAL_WIN_SOUND = os.path.join(os.path.dirname(
        __file__), '../assets/mixkit-clinking-coins-1993.wav')
    WIN_SOUND = os.path.join(os.path.dirname(
        __file__), '../assets/mixkit-coins-handling-1939.wav')
    BONUS_SOUND = os.path.join(os.path.dirname(
        __file__), '../assets/mixkit-magical-coin-win-1936.wav')
    ROLLING_SOUND = os.path.join(os.path.dirname(
        __file__), '../assets/mixkit-slot-machine-win-alert-1931.wav')
    NO_WIN_SOUND = os.path.join(os.path.dirname(
        __file__), '../assets/mixkit-thin-metal-card-deck-shuffle-3175.wav')
    
  
    def __init__(self, scr=None, context=None):
        self.scr = scr
        self.context = context
        self.game = None
        self.start_x = 0
        self.start_y = 0
        self.total_bonus_rounds = 0
        
        
    def display(self):
        for auto_plays in range(self.context['auto_play']):
          self.game = Game(wallet=self.context['account'].wallet, bet_value=self.context['bet_value'])         
          self.start_y = (self.context['height'] - len(self.game.slots.table)) // 3 
          self.start_x = (self.context['width'] // 2) - ((len(self.game.slots.table) // 2) * 7)
          self.total_bonus_rounds = 0
          
          self.scr.clear()
          self.scr.addstr(
              0, 0, f'🐲🐍🍀🤞🏽 Good Luck! 🤞🏽🍀🐍🐲')
          self.scr.addstr(
              1, 0, f'Balance: {(self.context['account'].wallet.balance - self.context['bet_value']) / 100} - Bet: ${self.context['bet_value'] / 100}')
          self.scr.addstr(
              2, 0, '3 or more Scatter symbols 💟 trigger bonus rounds! ')
          self.scr.addstr(
              3, 0, f'Auto plays: {auto_plays + 1}/{self.context['auto_play']}')
          self.scr.addstr(
              4, 0, f'Press CTRL+C to Stop')
          self.scr.refresh()

          self.play_sound(sound_file=self.ROLLING_SOUND, sync=False)
          for update in self.game.play():
            match update['action']:
              case 'fill_table' | 'find_clusters_and_update':
                self.update_table(data=update['data'])
              case 'win_symbol':
                self.win_symbol(data=update['data'])
              case 'tumble_table':
                self.tumble_table(data=update['data'])
              case 'prize':
                self.prize(data=update['data'])
              case 'bonus_rounds':
                self.bonus_rounds(data=update['data'])
              case 'round_n':
                self.round_n()
              case 'cash_in':
                self.cash_in(data=update['data'])
          
          self.scr.refresh()    
          self.scr.addstr(
              6, 0, f'Total Prize: ${self.game.total_win / 100}')
          curses.flash()
          time.sleep(self.context['speed'] + 0.5)

          self.context['last_game'] = self.game.slots.table
          self.context['last_prize'] = self.game.total_win / 100
          self.context['view'] = 'in_game'
        return self.context
      
      
    def update_table(self, data):
        for i in range(len(data)):
            for j in range(len(data)):
                self.scr.addstr(
                    self.start_y + i, self.start_x + (j * 6), f'｜ {str(data[i][j])} ')
            self.scr.refresh()
            self.sleep(additional=-0.4)
            curses.flash()
        self.scr.refresh()
        self.sleep(additional=0.5)
      
      
    def tumble_table(self, data):
        self.play_sound(sound_file=self.TUMBLING_SOUND, sync=False)
        self.update_table(data)
      
      
    def win_symbol(self, data={}):
        message = f'  Win {data['symbol']}x{data['size']} pays ${data['amount']}  '
        y = self.start_y + len(self.game.slots.table) + 2
        x = (self.context['width'] // 2) - (len(message) // 2)
        
        self.scr.refresh()
        self.scr.addstr(y, x, message)
        self.scr.refresh()
        self.play_sound(sound_file=self.WIN_SOUND)
        self.sleep(additional=0.8)
      
      
    def prize(self, data=0):
        message = f'  Total Win ${data}  '
        y = self.start_y + len(self.game.slots.table) + 1
        x = (self.context['width'] // 2) - (len(message) // 2)
        
        self.scr.refresh()
        self.scr.addstr(y, x, message)
        self.scr.refresh()
        self.play_sound(sound_file=self.TOTAL_WIN_SOUND)
        self.sleep(additional=0.5)
      
      
    def bonus_rounds(self, data=0):
        self.total_bonus_rounds += data
        message = f'  Congrats! You won {data} free spins!!  '
        y = self.start_y + len(self.game.slots.table) + 3
        x = (self.context['width'] // 2) - (len(message) // 2)
        
        self.scr.refresh()
        self.scr.addstr(y, x, message)
        self.scr.refresh()
        self.play_sound(sound_file=self.BONUS_SOUND)
        self.sleep(additional=1)
      
      
    def round_n(self):
        self.total_bonus_rounds -= 1
        message = f'  Remaining free spins: {self.total_bonus_rounds}  '
        y = self.start_y + len(self.game.slots.table) + 4
        x = (self.context['width'] // 2) - (len(message) // 2)
        
        self.scr.refresh()
        self.scr.refresh()
        self.scr.addstr(y, x, message)
    
    
    def cash_in(self, data=0):
        if data > 0:
          self.play_sound(sound_file=self.GAME_OVER_SOUND, sync=False)
          self.sleep()
        else:
          self.play_sound(sound_file=self.NO_WIN_SOUND, sync=False)
          self.sleep()
      
    
    def sleep(self, additional=0):
      if self.context['speed'] > 0 or additional > 0:
        time.sleep(self.context['speed'] + additional)
        
    def play_sound(self, sound_file=None, sync=True):
      if self.context['sounds_on']:
        playsound(sound_file, sync)