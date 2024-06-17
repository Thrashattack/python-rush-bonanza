import base64
import binascii
import crypt

from src.core.models.Player import Player
from src.infra.db.PlayerRepository import PlayerRepository
from src.infra.db.exceptions.NotFoundException import NotFoundException


class Auth(object):


    def authenticate(auth: str) -> str | bool:
        try:
            credentials = auth.split(" ")[1]
            name, password = base64.b64decode(credentials).decode('utf-8').split(':')
            encrypted = crypt.crypt(password, salt='NOT_SECURE')
            
            player = PlayerRepository.fetch_player(name=name, password=encrypted)
            
            return base64.b64encode(f'{player.name},{encrypted}'.encode('utf-8')).decode('utf-8')
        except (NotFoundException, TypeError, binascii.Error, UnicodeDecodeError):
            return False
        

    def validate_token(auth: str) -> Player:
        try:
            name, password = base64.b64decode(auth).decode('utf-8').split(',')
            
            return PlayerRepository.fetch_player(name=name, password=password)
        except (NotFoundException, TypeError, binascii.Error, UnicodeDecodeError):
            return False
