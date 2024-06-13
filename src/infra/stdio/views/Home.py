import curses
import time

from src.infra.stdio.use_cases.Account import Account

class Home(object):


    def __init__(self, scr=None, context=None):
        self.scr = scr
        self.context = context
        self.operations = {
            '\n': lambda name, password: self.signin(name=name, password=password),
            's': lambda name, password: self.signup(name=name, password=password)
        }
    
    
    def display(self):
        self.scr.addstr(
            0, 0, '🐲🐍 Welcome to Python Rush Bonanza 🐍🐲')
        self.scr.addstr(
            1, 0, 'Press Enter to Sign In →')
        self.scr.addstr(
            2, 0, 'Press S to Sign Up ↑')
        self.scr.addstr(
            3, 0, 'Press Q to Quit 👋🏽')
        self.scr.refresh()
        key = self.scr.getkey()
        self.scr.refresh()
        if key in self.operations:
            self.scr.addstr(
                4, 0, 'Type your username: 👩🏽‍💻\n')
            self.scr.refresh()
            curses.echo()
            name = self.scr.getstr().decode('utf-8')
            self.scr.addstr(
                5, 0, 'Type your password: 🔐\n')
            self.scr.refresh()
            curses.noecho()
            password = self.scr.getstr().decode('utf-8')
            return self.operations[key](name=name, password=password)
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
          
    def signin(self, name: str, password: str):
        self.context['account'] = Account(name=name, password=password)
        self.context['account'].signin()
        self.context['view'] = 'menu'
        return self.context


    def signup(self, name: str, password: str):
        self.context['account'] = Account(name=name, password=password)
        self.context['account'].signup()
        self.context['view'] = 'menu'
        return self.context