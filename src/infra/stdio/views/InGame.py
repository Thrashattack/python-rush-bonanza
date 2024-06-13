import time
import curses

class InGame(object):
  
  
    def __init__(self, scr=None, context=None):
        self.scr = scr
        self.context = context
        self.operations = {
            'm': lambda _: self.menu(),
            'b': lambda _: None,
            't': lambda _: None,
            ' ': lambda _: self.play(),
            'a': lambda _: self.set_auto_play()
        }
        
        
    def display(self):
        self.scr.addstr(
            0, 0, f'🐲🐍🎰 Python Rush Bonanza 🎰🐍🐲')
        self.scr.addstr(
            1, 0, 'Press Space to start betting 🎰')
        self.scr.addstr(
            2, 0, 'Press B to adjust the bet value 💰')
        self.scr.addstr(
            3, 0, 'Press M to Quit to Main Menu 👋🏽')
        self.scr.addstr(
            4, 0, f'Press A to adjust the auto play (Current auto play {self.context['auto_play']}) 🤖')
        self.scr.addstr(
            5, 0, f'Balance: {self.context['account'].wallet} - Bet: ${self.context['bet_value'] / 100}')
        self.scr.addstr(
            6, 0, f'Press T to toggle Turbo Mode 🏎️  - Turbo On? {self.context['speed'] == 0}')
        self.scr.addstr(
            7, 0, f'Last Prize 🤑 - ${self.context['last_prize']}')
        if self.context['last_game']:
            start_y = (self.context['height'] - len(self.context['last_game'])) // 3
            start_x = (self.context['width'] // 2) - ((len(self.context['last_game']) // 2) * 7)
            for i in range(len(self.context['last_game'])):
                for j in range(len(self.context['last_game'])):
                    self.scr.addstr(
                        start_y + i, start_x + j * 6, f'｜ {str(self.context['last_game'][i][j])} ')

        self.scr.refresh()
        key = self.scr.getkey()
        if key in self.operations:
            if key == 'b':
                self.scr.addstr(
                    8, 0, 'Type the new Bet Value 💶\n')
                curses.echo()
                self.scr.refresh()
                value = self.scr.getstr().decode('utf-8')
                return self.set_bet_value(bet=(float(value) * 100) // 1)
            elif key == 't':
                return self.toggle_turbo()
            else:
                return self.operations[key](None)
        else:
            self.scr.clear()
            self.scr.addstr(
                4, 0, f'Error - Unknown Operation 😳 ({key})')
            self.scr.refresh()
            time.sleep(2)
            return self.context
    
    def menu(self):
        self.context['view'] = 'menu'
        return self.context
      
    def play(self):
        self.context['view'] = 'playing'
        return self.context

    def set_auto_play(self):
        self.scr.addstr(
            8, 0, f'Enter the number of automatic plays: ')
        curses.echo()
        self.scr.refresh()
        value = self.scr.getstr().decode('utf-8')
        self.context['auto_play'] = int(value)
        curses.noecho()
        self.context['view'] = 'in_game'
        return self.context

    def toggle_turbo(self):
        if self.context['speed'] == 0.5:
            self.context['speed'] = 0
        else:
            self.context['speed'] = 0.5
        return self.context


    def set_bet_value(self, bet: int):
        self.context['bet_value'] = bet
        return self.context