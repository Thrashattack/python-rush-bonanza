from .connection import connect


def migrate():
    connection = connect()
    cursor = connection.cursor()

    print("Starting database migration 🛫")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players(
      id INTEGER PRIMARY KEY,
      name VARCHAR(50) NOT NULL UNIQUE,
      password VARCHAR(128) NOT NULL
    )
  """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallets(
      id INTEGER PRIMARY KEY,
      player_id INT NOT NULL UNIQUE,
      balance INT NOT NULL,
      FOREIGN KEY (player_id) REFERENCES players (id)
    )
  """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bet_transactions(
      id INTEGER PRIMARY KEY,
      wallet_id INT NOT NULL,
      operation VARCHAR(10) NOT NULL,
      value INT NOT NULL,
      timestamp DATETIME NOT NULL,
      FOREIGN KEY (wallet_id) REFERENCES wallets (id)
    )
  """)

    connection.commit()
    print("Database migrated successfully! 🛩️")
