from src.core.models.Wallet import Wallet
from .sqlite.connection import connect
from .exceptions.NotFoundException import NotFoundException


class WalletRepository(object):
    def fetch_wallet(player_id: int):
        with connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, balance FROM wallets WHERE player_id = ?",
                (player_id,))
            connection.commit()
            wallet = cursor.fetchone()
            if wallet:
                wallet_id, balance = wallet
                return Wallet(
                    id=wallet_id,
                    player_id=player_id,
                    balance=float("{:.0f}".format(balance)))
            else:
                raise NotFoundException(entity='Wallet', id=str(player_id))

    def create_wallet(player_id: int, balance=1000000):
        with connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO wallets(player_id, balance) VALUES (?, ?)",
                (player_id, balance))
            connection.commit()
            return WalletRepository.fetch_wallet(player_id=player_id)

    def update_balance(balance: int, wallet_id: int):
        with connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE wallets SET balance = ? WHERE player_id = ?",
                (balance, wallet_id))
            connection.commit()
