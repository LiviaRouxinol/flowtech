import mysql.connector
from conectar import connect_db

def insert_funcionario(dados):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO funcionario (nome, CPF, e_mail, setor, salario, turno, senha) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (dados ['nome'], dados['CPF'], dados['e_mail'], dados['salario'], dados['setor'], dados['turno'], dados['senha'])
            print(values)
            cursor.execute(sql, values)
            conn.commit()
            return {'status': 'sucesso', 'mensagem':'funcionario criado com sucesso' }
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f'erro ao criar funcionario: {err}'}
        finally:
            cursor.close()
            conn.close
