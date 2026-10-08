"""
database.py

Projeto IoT SENAI

Responsável por:
- conexão com MySQL;
- criação da tabela;
- gravação das leituras;
- consulta das leituras.

Sensores suportados:
- DHT11
- HC-SR04
- MFRC522
"""

from mysql.connector import pooling


# =====================================================
# CONFIGURACAO DO BANCO
# =====================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "sensores_db",
}


# =====================================================
# POOL DE CONEXOES
# =====================================================

pool = pooling.MySQLConnectionPool(
    pool_name="pool_sensores",
    pool_size=5,
    **DB_CONFIG
)


# =====================================================
# CRIAR TABELA
# =====================================================

def criar_tabela():

    conn = None
    cursor = None

    try:

        conn = pool.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS leituras (
                id INT AUTO_INCREMENT PRIMARY KEY,

                device_id VARCHAR(50) NOT NULL,

                sensor VARCHAR(30) NOT NULL,

                temperatura FLOAT NULL,

                umidade FLOAT NULL,

                distancia FLOAT NULL,

                rfid_uid VARCHAR(50) NULL,

                timestamp DATETIME NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()

        print(
            "Tabela 'leituras' verificada/criada com sucesso."
        )


    except Exception as erro:

        print(
            "Erro ao criar tabela:"
        )

        print(erro)

        raise


    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


# =====================================================
# SALVAR LEITURA
# =====================================================

def salvar_leitura(
    device_id,
    sensor,
    temperatura=None,
    umidade=None,
    distancia=None,
    rfid_uid=None
):

    conn = None
    cursor = None

    try:

        conn = pool.get_connection()

        cursor = conn.cursor()

        sql = """
            INSERT INTO leituras
            (
                device_id,
                sensor,
                temperatura,
                umidade,
                distancia,
                rfid_uid
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        valores = (
            device_id,
            sensor,
            temperatura,
            umidade,
            distancia,
            rfid_uid
        )

        cursor.execute(
            sql,
            valores
        )

        conn.commit()

        print(
            f"Leitura salva: "
            f"{device_id} | {sensor}"
        )

        return True


    except Exception as erro:

        print(
            "Erro ao salvar leitura:"
        )

        print(erro)

        return False


    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


# =====================================================
# LISTAR LEITURAS
# =====================================================

def listar_leituras(
    device_id=None,
    sensor=None,
    limite=100
):

    conn = None
    cursor = None

    try:

        # ---------------------------------------------
        # Protecao simples para o LIMIT
        # ---------------------------------------------

        limite = int(limite)

        if limite < 1:
            limite = 1

        if limite > 1000:
            limite = 1000


        conn = pool.get_connection()

        cursor = conn.cursor(
            dictionary=True
        )


        # ---------------------------------------------
        # MONTA A CONSULTA
        # ---------------------------------------------

        sql = """
            SELECT
                id,
                device_id,
                sensor,
                temperatura,
                umidade,
                distancia,
                rfid_uid,
                timestamp

            FROM leituras
        """

        filtros = []

        valores = []


        # ---------------------------------------------
        # FILTRO DEVICE
        # ---------------------------------------------

        if device_id:

            filtros.append(
                "device_id = %s"
            )

            valores.append(
                device_id
            )


        # ---------------------------------------------
        # FILTRO SENSOR
        # ---------------------------------------------

        if sensor:

            filtros.append(
                "sensor = %s"
            )

            valores.append(
                sensor
            )


        # ---------------------------------------------
        # WHERE
        # ---------------------------------------------

        if filtros:

            sql += " WHERE "

            sql += " AND ".join(
                filtros
            )


        # ---------------------------------------------
        # ORDENACAO E LIMITE
        # ---------------------------------------------

        sql += """
            ORDER BY timestamp DESC, id DESC
            LIMIT %s
        """

        valores.append(
            limite
        )


        cursor.execute(
            sql,
            tuple(valores)
        )

        resultado = cursor.fetchall()

        return resultado


    except Exception as erro:

        print(
            "Erro ao listar leituras:"
        )

        print(erro)

        return []


    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


# =====================================================
# TESTE DIRETO DO ARQUIVO
# =====================================================
#
# Esta parte só roda quando executamos:
#
# python database.py
#
# Quando o FastAPI importar este arquivo,
# ela NÃO será executada.
#

if __name__ == "__main__":

    print()
    print("================================")
    print("   TESTE DATABASE - SENAI")
    print("================================")

    print()
    print("Testando conexao com MySQL...")


    # =================================================
    # CRIAR / VERIFICAR TABELA
    # =================================================

    criar_tabela()


    # =================================================
    # TESTE DHT11
    # =================================================

    print()
    print("Inserindo teste DHT11...")

    salvar_leitura(
        device_id="esp32-teste",
        sensor="DHT11",
        temperatura=25,
        umidade=60
    )


    # =================================================
    # TESTE HC-SR04
    # =================================================

    print()
    print("Inserindo teste HC-SR04...")

    salvar_leitura(
        device_id="esp32-teste",
        sensor="HC-SR04",
        distancia=38.50
    )


    # =================================================
    # TESTE MFRC522
    # =================================================

    print()
    print("Inserindo teste MFRC522...")

    salvar_leitura(
        device_id="esp32-teste",
        sensor="MFRC522",
        rfid_uid="TESTE-01-02-03"
    )


    # =================================================
    # CONSULTAR
    # =================================================

    print()
    print("================================")
    print("LEITURAS GRAVADAS")
    print("================================")

    leituras = listar_leituras(
        device_id="esp32-teste",
        limite=10
    )


    for leitura in leituras:

        print()
        print(leitura)


    print()
    print("================================")
    print("TESTE FINALIZADO")
    print("================================")