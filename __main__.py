import os
from src.infra.stdio.Repl import Repl
from src.infra.db.sqlite.migrations import migrate

if __name__ == '__main__':
    os.system(f'printf "\\e[8;{36};{100}t"')  # Terminal Size

    migrate()
    
    Repl().bootstrap()
