import sys
import os
from src.infra.stdio.Repl import Repl
from src.infra.db.sqlite.migrations import migrate

if __name__ == '__main__':
    match sys.argv[1]:
        case '--stdio':
            migrate()
            Repl().bootstrap()
        case '--http':
            migrate()
            match sys.argv[2]:
                case '--dev':
                    os.system('fastapi dev src/infra/http/api.py')
                case '--prod':
                    os.system('fastapi run src/infra/http/api.py')
        case '--help' | _:
            print("PYTHON GEMS BONANZA")
            print("Usage: python3 . [--stdio|--http[--dev|--prod]|--help]")
            print("--stdio: Run the shell (terminal) game")
            print("--http --dev: Run the Web game in dev mode")
            print("--http --run: Run the Web game in prod mode")
            print("--help: Print this help message")
