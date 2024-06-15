from sqlite3 import IntegrityError
from src.core.models.Player import Player
from src.infra.db.exceptions.AlreadyExistsException import AlreadyExistsException
from .sqlite.connection import connect
from .exceptions.NotFoundException import NotFoundException


class PlayerRepository(object):
    def fetch_player(name: str, password: str) -> Player:
        with connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, name FROM players WHERE name = ? AND password = ?", (str(name), str(password)))
            connection.commit()
            player = cursor.fetchone()
            if player:
                player_id, _ = player
                return Player(id=int(player_id), name=name)
            else:
                raise NotFoundException(entity='Player', id=name)

    def create_player(name: str, password: str) -> Player:
        try:
            with connect() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO players(name, password) VALUES (?, ?)", (str(name), str(password)))
                connection.commit()
            return PlayerRepository.fetch_player(name=name, password=password)
        except IntegrityError:
            raise AlreadyExistsException(entity='Player', id=name)
