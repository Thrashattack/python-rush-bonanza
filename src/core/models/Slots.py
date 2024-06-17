import functools
import operator
from random import randrange
from collections import deque
from src.core.models.Symbol import Symbol
from src.core.models.WinCluster import WinCluster


class Slots(object):
    """
        Slots Machine Implementation\n
        The Variance is given by the difference of the payouts for each symbol.\n
        On default configuration the highest paying symbol pays 100% of the bet and the lowest 10%. Therefore a High variance.\n
        The RTP is calculated over time with monte carlo simulations and is asserted through behavioral tests to be between 87% and 97%\n
        The Volatility is given by the Lucky Symbol chance combined with each symbol chance.\n
        On default configuration the chance of lucky symbol is 20% and the highest paying symbol chance is 3.50% yielding a low volatility
    """
    SCATTER_SYMBOL = Symbol(value=1, symbol='💟')
    WIN_SYMBOL = Symbol(value=0, symbol='🔥')
    EMPTY_SYMBOL = Symbol(value=0, symbol=' ')
    SCATTER_SYMBOL_CHANCE = 100                             # 1% 1/100
    LUCKY_SYMBOL_CHANCE = 5                                 # 20% 1/5
    SCATTER_SYMBOL_INDEX = 1                                # Arbitrary index
    LUCKY_SYMBOL_INDEX = 1                                  # Arbitrary index
    DEFAULT_SIZE = 7                                        # 7x7 table
    DEFAULT_SYMBOLS = functools.reduce(operator.iconcat, [
        [Symbol(value=100, symbol='🐍')]    * 1,            # 3.50%  1/28
        [Symbol(value=75, symbol='🦎')]     * 2,            # 7.14%  2/28
        [Symbol(value=50, symbol='🐁')]     * 3,            # 10.71% 3/28
        [Symbol(value=70, symbol='🐣')]     * 4,            # 14.28% 4/28
        [Symbol(value=10, symbol='🦂')]     * 5,            # 17.85% 5/28
        [Symbol(value=25, symbol='🦋')]     * 6,            # 21.42% 6/28
        [Symbol(value=20, symbol='🐞')]     * 7,            # 25%    7/28
    ], [])
    MIN_SCATTER_TO_BONUS = 3                                # 3.51% when scatter is 1% chance per tile (binomial distribution)
    BONUS_PER_SCATTER = {
        '3': 8,
        '4': 10,
        '5': 12,
        '6': 15,
        '7': 20,
    }

    def __init__(self, odds=DEFAULT_SYMBOLS, size=DEFAULT_SIZE, scatter=SCATTER_SYMBOL):
        self.odds = odds
        self.size = size
        self.table = [
            [scatter for _ in range(size)] for _ in range(size)]
        self.wins = []
        self.visited = []
        self.scatter_count = 0
        self.scatter_symbol = scatter

    def fill_table(self, only_empty=False):
        """
            Fill the table tiles with symbols.
            When only_empty is settled, only fills empty tiles
            For each tile, it will check if it will be a Scatter symbol by calling is_scatter()
            When it's not a Scatter, it will check if it will be the chosen lucky symbol by calling is_lucky()
        """
        lucky_symbol = self.odds[randrange(len(self.odds))]
        for i in range(self.size):
            for j in range(self.size):
                if only_empty and self.table[j][i] != self.EMPTY_SYMBOL:
                    continue
                elif self.is_scatter():
                    self.table[j][i] = self.scatter_symbol
                    self.scatter_count += 1
                elif self.is_lucky():
                    self.table[j][i] = lucky_symbol
                else:
                    self.table[j][i] = self.odds[randrange(len(self.odds))]
                        
    def is_lucky(self):
        """
            Randomly pick a number within the lucky symbol range and compare with the chosen lucky index
        """
        return randrange(self.LUCKY_SYMBOL_CHANCE) == self.LUCKY_SYMBOL_INDEX

    def is_scatter(self):
        """
            Randomly pick a number within the scatter symbol range and compare with the chosen scatter index
        """
        return randrange(self.SCATTER_SYMBOL_CHANCE) == self.SCATTER_SYMBOL_INDEX

    def is_valid(self, row: int, column: int, symbol: Symbol):
        """
            Checks if the tile is valid for the cluster search by verifying if its under the matrix limits
            Also checks if it wasn't already visited and if its equal the symbol currently being searched for
            For sanity check it also checks if it's not a scatter symbol and a win symbol
        """
        return (0 <= row < self.size and
                0 <= column < self.size and
                not (row, column) in self.visited and
                self.table[row][column] == symbol and
                symbol != self.scatter_symbol and 
                symbol != self.WIN_SYMBOL)

    def bfs_cluster_size(self, start_row: int, start_column: int, symbol: Symbol):
        """
            Use Breadth-first search (BFS) to search for matching symbols
            with the condition of being clustered vertically or horizontally.
            return an array of coordinates for each matching symbol and the size of the cluster
        """
        queue = deque([(start_row, start_column)])
        cluster_coords = []
        size = 0

        while queue:
            row, column = queue.popleft()
            if not self.is_valid(row=row, column=column, symbol=symbol):
                continue

            self.visited.append((row, column))
            cluster_coords.append((row, column))
            size += 1

            # Add all valid neighboring positions to the queue
            # Up, Down, Left, Right
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                new_row, new_column = row + dr, column + dc
                if self.is_valid(new_row, new_column, symbol):
                    queue.append((new_row, new_column))

        return size, cluster_coords

    def find_clusters_and_update(self):
        """
            For each tile in the table, will perform a BFS search to obtain the size of the cluster
            and the coordinates of the matching tiles. 
            If the size is enough to a win, it will add the win to the list of wins
            and replace the cluster with WIN_SYMBOL
        """
        for row in range(self.size):
            for column in range(self.size):
                symbol = self.table[row][column]
                size, cluster_coords = self.bfs_cluster_size(
                    row, column, symbol)
                if size >= WinCluster.MIN_TO_WIN:
                    self.wins.append(WinCluster(
                        symbol=symbol, size=size, start=[row, column]))
                    for r, c in cluster_coords:
                        self.table[r][c] = self.WIN_SYMBOL

    def bonus_game(self):
        """
            Evaluate the number of SCATTER_SYMBOL in the current table state 
            When it's enough to a bonus round, calculate the number of bonus rounds and return it
        """
        if self.scatter_count < self.MIN_SCATTER_TO_BONUS:
            return False

        if self.scatter_count > self.size:
            self.scatter_count = self.size

        return self.BONUS_PER_SCATTER[str(self.scatter_count)]

    def tumble_table(self):
        """
            Tumbling (falling) algorithm will perform a column based search on the table
            For each column it declares two pointers (bot and top) and a temporary new column
            For each line it will check if its a normal symbol or a win symbol and place them
            accordingly in the new column.
            Normal symbols should be places as low as possible in the column
            and winning symbols should go all the way
        """
        for j in range(self.size):
            top_pointer = 0
            bottom_pointer = self.size - 1
            temp_col = [None] * self.size  # new column

            for i in reversed(range(self.size)):
                if self.table[i][j] == self.WIN_SYMBOL:
                    temp_col[top_pointer] = self.EMPTY_SYMBOL
                    top_pointer += 1
                else:
                    temp_col[bottom_pointer] = self.table[i][j]
                    bottom_pointer -= 1

            for i in range(self.size):  # Merge new column to table
                self.table[i][j] = temp_col[i]
