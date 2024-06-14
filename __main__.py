import sys
from src.infra.http.Api import Api
from src.infra.stdio.Repl import Repl
from src.infra.db.sqlite.migrations import migrate

if __name__ == '__main__':
    match sys.argv[1]:
        case '--stdio':
            migrate()
            Repl().bootstrap()
        case '--http':
            migrate()
            Api()
        case '--help' | _:
            print("PYTHON GEMS BONANZA")
            print("Usage: python3 . [--stdio|--http|--help]")
            print("--stdio: Run the shell (terminal) game")
            print("--http: Run the Web game")
            print("--help: Print this help message")
