import base64
import binascii
import crypt
from src.core.models.Player import Player
from src.core.models.Wallet import Wallet
from src.infra.db.WalletRepository import WalletRepository
from src.infra.db.PlayerRepository import PlayerRepository
from src.infra.db.exceptions.AlreadyExistsException import AlreadyExistsException
from src.infra.http.use_cases.Auth import Auth


class Account(object):


    def create_player(auth: str) -> Player:
        try:
            credentials = auth.split(" ")[1]
            name, password = base64.b64decode(credentials).decode('utf-8').split(':')
            encrypted = crypt.crypt(password, salt='NOT_SECURE')
            player = PlayerRepository.create_player(name=name, password=encrypted)
            WalletRepository.create_wallet(player_id=player.id)
            
            return Auth.authenticate(f'Basic {base64.b64encode(f'{name}:{password}'.encode('utf-8')).decode('utf-8')}')
        except (AlreadyExistsException, TypeError, binascii.Error, UnicodeDecodeError):
            return False


    def get_player_wallet(player_id: int) -> Wallet:
        return WalletRepository.fetch_wallet(player_id=player_id)


    def update_balance(balance: int, wallet_id: int) -> None:
        return WalletRepository.update_balance(balance=balance, wallet_id=wallet_id)