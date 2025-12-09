import mysql.connector
from conectar import connect_db

def delete_funcionario(funcionario_id):
    conn= connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            sql ="DELETE FROM funcionario WHERE funcionario_id = %s"
            cursor.execute(sql,(funcionario_id,))
            conn.commit()
            return{'status': 'sucesso', 'mensagem': f'Funcionário{funcionario_id} excluído com sucesso'}
        except mysql.connector.Error as err:
            return{'status': 'erro', 'mensagem': f'Erro ao excluir o funcionário:{err}'}
        finally:
            cursor.close()
            conn.close()


