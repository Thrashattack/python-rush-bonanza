import sqlite3


def connect():
    return sqlite3.connect("python_rush_bonanza.db")
