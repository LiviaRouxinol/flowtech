"""
mqtt_manager.py

Projeto IoT SENAI

Responsavel pela integracao:

ESP32
  ↓
HiveMQ Cloud
  ↓
MQTT Manager
  ↓
database.py
  ↓
MySQL

Sensores suportados:
- DHT11
- HC-SR04
- MFRC522
"""

import json
import logging
import ssl
import uuid

import certifi
import paho.mqtt.client as mqtt

from database import salvar_leitura


# =====================================================
# LOG
# =====================================================

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(
    "mqtt_manager"
)


# =====================================================
# CONFIGURACOES MQTT
# =====================================================

MQTT_BROKER = (
    "b1600c60a35c4520b32b9507d0b47b02"
    ".s1.eu.hivemq.cloud"
)

MQTT_PORT = 8883

MQTT_USER = "IOT-SENAI"
MQTT_PASSWORD = "12345678"

MQTT_TOPIC = "sensores/leitura"

MQTT_CLIENT_ID = f"fastapi-backend-{uuid.uuid4().hex[:8]}"


# =====================================================
# CLASSE MQTT MANAGER
# =====================================================

class MQTTManager:

    def __init__(self):

        # ---------------------------------------------
        # Criar cliente MQTT
        # ---------------------------------------------

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
            client_id=MQTT_CLIENT_ID,
            protocol=mqtt.MQTTv311
        )


        # ---------------------------------------------
        # Usuario e senha
        # ---------------------------------------------

        self.client.username_pw_set(
            MQTT_USER,
            MQTT_PASSWORD
        )


        # ---------------------------------------------
        # TLS
        # ---------------------------------------------

        self.client.tls_set(
            ca_certs=certifi.where(),
            tls_version=ssl.PROTOCOL_TLS_CLIENT
        )


        # ---------------------------------------------
        # Callbacks
        # ---------------------------------------------

        self.client.on_connect = (
            self.on_connect
        )

        self.client.on_message = (
            self.on_message
        )

        self.client.on_disconnect = (
            self.on_disconnect
        )


    # =================================================
    # CONEXAO REALIZADA
    # =================================================

    def on_connect(
        self,
        client,
        userdata,
        flags,
        rc
    ):

        if rc == 0:

            print()
            print("================================")
            print("BACKEND CONECTADO AO HIVEMQ")
            print("================================")

            print()
            print("Topico:")
            print(MQTT_TOPIC)


            client.subscribe(
                MQTT_TOPIC,
                qos=1
            )


            print()
            print(
                "Aguardando dados dos sensores..."
            )


            logger.info(
                "Conectado ao HiveMQ."
            )

        else:

            print()
            print("ERRO MQTT")

            print(
                "Codigo:",
                rc
            )


            logger.error(
                "Falha MQTT. Codigo: %s",
                rc
            )


    # =================================================
    # DESCONEXAO
    # =================================================

    def on_disconnect(
        self,
        client,
        userdata,
        rc
    ):

        print()
        print(
            "MQTT desconectado. Codigo:",
            rc
        )


        logger.warning(
            "MQTT desconectado. rc=%s",
            rc
        )


    # =================================================
    # MENSAGEM RECEBIDA
    # =================================================

    def on_message(
        self,
        client,
        userdata,
        msg
    ):

        try:

            # -----------------------------------------
            # Decodificar mensagem
            # -----------------------------------------

            texto = msg.payload.decode(
                "utf-8"
            )


            dados = json.loads(
                texto
            )


            # -----------------------------------------
            # Dados comuns
            # -----------------------------------------

            device_id = dados.get(
                "device_id",
                "esp32-desconhecido"
            )


            sensor = dados.get(
                "sensor"
            )


            print()
            print("================================")
            print("NOVA LEITURA MQTT")
            print("================================")

            print(
                "Device:",
                device_id
            )

            print(
                "Sensor:",
                sensor
            )


            # =================================================
            # DHT11
            # =================================================

            if sensor == "DHT11":

                temperatura = dados.get(
                    "temperatura"
                )

                umidade = dados.get(
                    "umidade"
                )


                print(
                    "Temperatura:",
                    temperatura,
                    "C"
                )

                print(
                    "Umidade:",
                    umidade,
                    "%"
                )


                sucesso = salvar_leitura(

                    device_id=device_id,

                    sensor="DHT11",

                    temperatura=temperatura,

                    umidade=umidade
                )


            # =================================================
            # HC-SR04
            # =================================================

            elif sensor == "HC-SR04":

                distancia = dados.get(
                    "distancia"
                )


                print(
                    "Distancia:",
                    distancia,
                    "cm"
                )


                sucesso = salvar_leitura(

                    device_id=device_id,

                    sensor="HC-SR04",

                    distancia=distancia
                )


            # =================================================
            # MFRC522
            # =================================================

            elif sensor == "MFRC522":

                rfid_uid = dados.get(
                    "rfid_uid"
                )


                print(
                    "UID:",
                    rfid_uid
                )


                sucesso = salvar_leitura(

                    device_id=device_id,

                    sensor="MFRC522",

                    rfid_uid=rfid_uid
                )


            # =================================================
            # SENSOR DESCONHECIDO
            # =================================================

            else:

                print()
                print(
                    "Sensor nao reconhecido:"
                )

                print(
                    sensor
                )

                return


            # =================================================
            # RESULTADO
            # =================================================

            if sucesso:

                print(
                    "Banco de dados: GRAVADO"
                )

            else:

                print(
                    "Banco de dados: ERRO"
                )


        # =====================================================
        # JSON INVALIDO
        # =====================================================

        except json.JSONDecodeError:

            print()
            print(
                "Payload JSON invalido:"
            )

            print(
                msg.payload
            )


        # =====================================================
        # OUTRO ERRO
        # =====================================================

        except Exception as erro:

            print()
            print("================================")
            print("ERRO AO PROCESSAR MQTT")
            print("================================")

            print(
                "Tipo:",
                type(erro)
            )

            print(
                "Erro:",
                erro
            )


            logger.exception(
                "Erro processando mensagem MQTT."
            )


    # =================================================
    # INICIAR MQTT
    # =================================================

    def start(self):

        print()
        print("================================")
        print("INICIANDO MQTT MANAGER")
        print("================================")

        print()
        print("Broker:")
        print(MQTT_BROKER)

        print()
        print("Porta:")
        print(MQTT_PORT)

        print()
        print("Topico:")
        print(MQTT_TOPIC)

        print()
        print("Conectando...")


        self.client.connect(
            MQTT_BROKER,
            MQTT_PORT,
            keepalive=60
        )


        # Executa MQTT em outra thread.
        # Assim ele nao bloqueia o FastAPI.

        self.client.loop_start()


    # =================================================
    # PARAR MQTT
    # =================================================

    def stop(self):

        print()
        print("Parando MQTT Manager...")


        self.client.loop_stop()

        self.client.disconnect()


# =====================================================
# INSTANCIA UNICA
# =====================================================

mqtt_manager = MQTTManager()