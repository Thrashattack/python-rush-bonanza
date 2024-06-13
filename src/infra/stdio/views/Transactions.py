import time

class Transactions(object):
  
    def __init__(self, scr=None, context=None):
        self.scr = scr
        self.context = context
    
    def display(self):
        self.scr.addstr(
            0, 0, f'📈 Your 20 last transactions 💰')
        self.scr.addstr(
            2, 0, 'Press M to Quit to Menu')
        self.scr.addstr(
            3, 0, 'ID')
        self.scr.addstr(
            3, 7, 'VALUE')
        self.scr.addstr(
            3, 14, 'OP')
        self.scr.addstr(
            3, 21, 'DATE')
        self.context['account'].fetch_transactions()
        x = 5
        for transaction in self.context['account'].transactions:
            y = 0
            for column in transaction:
                if y == 7:
                    self.scr.addstr(
                        x, y, str(column / 100))
                else:
                    self.scr.addstr(
                        x, y, str(column))
                y += 7
            self.scr.refresh()
            time.sleep(0.1)
            x += 1

        rtp_data = self.context['account'].calc_rtp()
        self.scr.addstr(
            x, 0,
            f'Total wins: {rtp_data['credit'] / 100} | Total wager: ' +
            f'{rtp_data['debit'] / 100} | Balance: ' +
            f'{rtp_data['balance'] / 100}')
        self.scr.addstr(
            x+1, 0,
            f'Total of transactions (wins and losses): ' +
            f'{rtp_data['transactions']}')
        self.scr.refresh()
        key = self.scr.getkey()
        if key == 'm':
            self.context['view'] = 'menu'
            return self.context
        else:
            self.scr.clear()
            self.scr.addstr(
                4, 0, f'Error - Unknown Operation 😳 ({key})')
            self.scr.refresh()
            time.sleep(2)
            return self.context