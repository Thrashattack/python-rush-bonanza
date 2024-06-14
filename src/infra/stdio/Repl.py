import os
import time
import curses

from src.core.exceptions.InsufficientFundsException import InsufficientFundsException
from src.infra.db.exceptions.AlreadyExistsException import AlreadyExistsException

from src.infra.db.exceptions.NotFoundException import NotFoundException
from src.infra.stdio.views.Home import Home
from src.infra.stdio.views.InGame import InGame
from src.infra.stdio.views.Menu import Menu
from src.infra.stdio.views.Playing import Playing
from src.infra.stdio.views.Transactions import Transactions

class Repl(object):


    def __init__(self,):
        self.scr = curses.initscr()
        self.context = {
            'account': None,
            'game': None,
            'view': 'home',
            'bet_value': 10000,
            'last_game': None,
            'last_prize': 0,
            'auto_play': 1,
            'speed': 0.5,
            'sounds_on': True,
            'height': 0,
            'width': 0,
        }


    def bootstrap(self):
        os.system(f'printf "\\e[8;{36};{100}t"')  # Terminal Size
        self.scr.keypad(True)
        curses.curs_set(0)  # Hide the cursor
        curses.mousemask(-1)
        self.scr.clear()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, 208)
        self.scr.bkgd(' ', curses.color_pair(1))
        self.scr.refresh()

        while (True):
            try:
                self.scr.clear()
                self.scr.refresh()
                self.evaluate_and_print()
            except (
                    InsufficientFundsException,
                    AlreadyExistsException,
                    NotFoundException
                ) as exception:
                height, _ = self.scr.getmaxyx()
                self.scr.addstr(
                    height - 2, 0, str(type(exception).__name__))
                self.scr.addstr(
                    height - 1, 0, str(exception))
                self.scr.refresh()
                curses.flash()
                time.sleep(3.5)
                self.context['view'] = 'home'
                pass
            except KeyboardInterrupt:
                curses.flushinp()
                if self.context['view'] == 'playing':
                    self.context['view'] = 'in_game'
                    pass
                else:
                    exit()
            except Exception as e:
                raise e 


    def evaluate_and_print(self):
        curses.noecho()
        curses.flushinp()
        self.context['height'], self.context['width'] = self.scr.getmaxyx()

        match self.context['view']:
            case 'home':
                self.context = Home(scr=self.scr, context=self.context).display()
            case 'menu':
                self.context = Menu(scr=self.scr, context=self.context).display()
            case 'in_game':
                self.context = InGame(scr=self.scr, context=self.context).display()
            case 'playing':
                self.context = Playing(scr=self.scr, context=self.context).display()
            case 'transactions':
                self.context = Transactions(scr=self.scr, context=self.context).display()
            case _:
                self.context['view'] = 'menu'
