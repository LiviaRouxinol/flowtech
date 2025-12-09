import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "flowtech"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

