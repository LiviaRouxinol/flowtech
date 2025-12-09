import mysql.connector
from conectar import connect_db

# --- SELECT DE CLIENTES --- #
def read_funcionario():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM funcionario")
            resultados = cursor.fetchall()
            return {'status': 'sucesso', 'dados': resultados}
        except mysql.connector.Error as err:
            return {'status': 'sucesso', 'mensagem': f"Erro ao listar funcionário: {err}"}
        finally:
            cursor.close()
            conn.close()

