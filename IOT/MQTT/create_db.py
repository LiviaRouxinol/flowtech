"""
create_db.py

Projeto IoT SENAI

Este arquivo cria o banco de dados sensores_db.

Execute uma única vez antes do database.py.
"""

import mysql.connector


print()
print("================================")
print("   CRIACAO DO BANCO - SENAI")
print("================================")


conn = None
cursor = None


try:

    print()
    print("Conectando ao MySQL...")


    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456"
    )


    print("Conexao com MySQL realizada!")


    cursor = conn.cursor()


    # =================================================
    # CRIAR BANCO
    # =================================================

    print()
    print("Criando/verificando banco sensores_db...")


    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS sensores_db"
    )


    print()
    print("================================")
    print("BANCO CRIADO COM SUCESSO!")
    print("================================")

    print()
    print("Banco:")
    print("sensores_db")

    print()
    print("Agora execute:")
    print("python database.py")


except mysql.connector.Error as erro:

    print()
    print("================================")
    print("ERRO NO MYSQL")
    print("================================")

    print()
    print("Codigo:")
    print(erro.errno)

    print()
    print("Mensagem:")
    print(erro)


except Exception as erro:

    print()
    print("================================")
    print("ERRO")
    print("================================")

    print()
    print(type(erro))

    print()
    print(erro)


finally:

    if cursor is not None:

        cursor.close()


    if conn is not None:

        if conn.is_connected():

            conn.close()


    print()
    print("Conexao encerrada.")