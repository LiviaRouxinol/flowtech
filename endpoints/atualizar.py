import mysql.connector
from conectar import connect_db

def update_funcionario(dados):
    print('Banco',dados)
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE funcionario SET nome = %s, CPF= %s,e_mail= %s, salario= %s, setor =%s, turno= %s, senha= %s WHERE funcionario_id = %s"
            values = (dados ['nome'], dados['CPF'], dados['e_mail'], dados['salario'], dados['setor'], dados['turno'], dados['senha'], dados ['funcionario_id'])
            print(values)
            cursor.execute(sql, values)
            conn.commit()
            return{'status': 'sucesso', 'mensagem': f"Funcionário {dados ['funcionario_id']} atualizado com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'error', 'mensagem': f"Erro ao atualizar funcionário: {err}"}
        finally:
            cursor.close()
            conn.close()
        
