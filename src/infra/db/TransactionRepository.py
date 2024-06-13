from .sqlite.connection import connect
from .exceptions.NotFoundException import NotFoundException
import time


class TransactionRepository(object):
    def fetch_transactions(wallet_id: int, limit: int = 20):
        with connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
              "SELECT id, value, operation, timestamp FROM bet_transactions WHERE wallet_id = ? ORDER BY id DESC LIMIT ?",
              (wallet_id, limit))
            connection.commit()
            transactions = cursor.fetchall()
            if transactions:
                return transactions
            else:
                raise NotFoundException(
                    entity='Transaction', id=str(wallet_id))

    def create_transaction(
            wallet_id: int,
            value: int,
            operation: str,
            timestamp=time.ctime()
    ):
        with connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
              "INSERT INTO bet_transactions(wallet_id, value, operation, timestamp) VALUES (?, ?, ?, ?)",
              (wallet_id, value, operation, timestamp))
            connection.commit()
