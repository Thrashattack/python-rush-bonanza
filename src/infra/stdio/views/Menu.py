import time


class Menu(object):
  
  
    def __init__(self, scr=None, context=None):
        self.scr = scr
        self.context = context
        self.operations = {
            '\n': lambda _: self.game(),
            't': lambda _: self.transactions()
        }
    
    
    def display(self):
        self.scr.addstr(
            0, 0, f'🐲🐍 Welcome {self.context["account"].name}! Let\'s make money 🐍🐲')
        self.scr.addstr(
            1, 0, 'Press Enter to Play 🃏')
        self.scr.addstr(
            2, 0, 'Press T to access your transactions 📊')
        self.scr.addstr(
            3, 0, 'Press Q to Quit 👋🏽')
        self.scr.refresh()
        key = self.scr.getkey()
        if key in self.operations:
            return self.operations[key](None)
        if key == 'q':
            self.scr.addstr(
                4, 0, 'Bye! 😘')
            self.scr.refresh()
            return exit()
        else:
            self.scr.clear()
            self.scr.addstr(
                4, 0, f'Error - Unknown Operation 😳 ({key})')
            self.scr.refresh()
            time.sleep(2)
            return self.context
          
    def game(self):
        self.context['view'] = 'in_game'
        return self.context


    def transactions(self):
        self.context['view'] = 'transactions'
        return self.context