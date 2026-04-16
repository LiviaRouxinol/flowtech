import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:
    @staticmethod
    def connect():
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            raise Exception(f"Falha na conexão com o banco de dados: {e}")
