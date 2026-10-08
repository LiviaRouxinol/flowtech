"""
main.py

API IoT - SENAI

Arquitetura:

ESP32
   ↓
HiveMQ Cloud
   ↓
MQTT Manager
   ↓
MySQL
   ↓
FastAPI
   ↓
Navegador / Aplicacao

Sensores:
- DHT11
- HC-SR04
- MFRC522
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Query

from mqtt_manager import mqtt_manager
from database import criar_tabela, listar_leituras


# =====================================================
# CICLO DE VIDA DA API
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print()
    print("================================")
    print("   API IoT SENAI")
    print("================================")

    print()
    print("Inicializando banco de dados...")


    # -------------------------------------------------
    # Garante que a tabela existe
    # -------------------------------------------------

    criar_tabela()


    print()
    print("Inicializando MQTT Manager...")


    # -------------------------------------------------
    # Conecta ao HiveMQ
    # -------------------------------------------------

    mqtt_manager.start()


    print()
    print("================================")
    print("SISTEMA INICIALIZADO")
    print("================================")

    print()
    print("FastAPI: OK")
    print("MySQL:   OK")
    print("MQTT:    iniciando")

    print()
    print(
        "Aguardando dados dos sensores..."
    )


    # -------------------------------------------------
    # FastAPI fica executando
    # -------------------------------------------------

    yield


    # -------------------------------------------------
    # Quando a API for encerrada
    # -------------------------------------------------

    print()
    print("Encerrando sistema...")


    mqtt_manager.stop()


    print(
        "Sistema encerrado."
    )


# =====================================================
# CRIAR FASTAPI
# =====================================================

app = FastAPI(

    title="API IoT SENAI",

    description=(
        "API para monitoramento dos sensores "
        "DHT11, HC-SR04 e MFRC522."
    ),

    version="1.0.0",

    lifespan=lifespan
)


# =====================================================
# ROTA PRINCIPAL
# =====================================================

@app.get("/")
def root():

    return {

        "status": "online",

        "projeto": "IoT SENAI",

        "mqtt": "ativo",

        "sensores": [
            "DHT11",
            "HC-SR04",
            "MFRC522"
        ]

    }


# =====================================================
# LISTAR LEITURAS
# =====================================================

@app.get("/leituras")
def get_leituras(

    device_id: str = None,

    sensor: str = None,

    limite: int = Query(
        default=100,
        ge=1,
        le=1000
    )

):

    resultado = listar_leituras(

        device_id=device_id,

        sensor=sensor,

        limite=limite

    )


    return {

        "quantidade": len(resultado),

        "filtros": {

            "device_id": device_id,

            "sensor": sensor,

            "limite": limite

        },

        "leituras": resultado

    }


# =====================================================
# ROTA DHT11
# =====================================================

@app.get("/sensores/dht11")
def get_dht11(

    device_id: str = None,

    limite: int = Query(
        default=100,
        ge=1,
        le=1000
    )

):

    resultado = listar_leituras(

        device_id=device_id,

        sensor="DHT11",

        limite=limite

    )


    return {

        "sensor": "DHT11",

        "quantidade": len(resultado),

        "leituras": resultado

    }


# =====================================================
# ROTA HC-SR04
# =====================================================

@app.get("/sensores/hc-sr04")
def get_hcsr04(

    device_id: str = None,

    limite: int = Query(
        default=100,
        ge=1,
        le=1000
    )

):

    resultado = listar_leituras(

        device_id=device_id,

        sensor="HC-SR04",

        limite=limite

    )


    return {

        "sensor": "HC-SR04",

        "quantidade": len(resultado),

        "leituras": resultado

    }


# =====================================================
# ROTA MFRC522
# =====================================================

@app.get("/sensores/mfrc522")
def get_mfrc522(

    device_id: str = None,

    limite: int = Query(
        default=100,
        ge=1,
        le=1000
    )

):

    resultado = listar_leituras(

        device_id=device_id,

        sensor="MFRC522",

        limite=limite

    )


    return {

        "sensor": "MFRC522",

        "quantidade": len(resultado),

        "leituras": resultado

    }


# =====================================================
# ULTIMA LEITURA DHT11
# =====================================================

@app.get("/sensores/dht11/ultima")
def ultima_dht11(

    device_id: str = None

):

    resultado = listar_leituras(

        device_id=device_id,

        sensor="DHT11",

        limite=1

    )


    if not resultado:

        return {

            "sensor": "DHT11",

            "leitura": None

        }


    return {

        "sensor": "DHT11",

        "leitura": resultado[0]

    }


# =====================================================
# ULTIMA LEITURA HC-SR04
# =====================================================

@app.get("/sensores/hc-sr04/ultima")
def ultima_hcsr04(

    device_id: str = None

):

    resultado = listar_leituras(

        device_id=device_id,

        sensor="HC-SR04",

        limite=1

    )


    if not resultado:

        return {

            "sensor": "HC-SR04",

            "leitura": None

        }


    return {

        "sensor": "HC-SR04",

        "leitura": resultado[0]

    }


# =====================================================
# ULTIMA LEITURA RFID
# =====================================================

@app.get("/sensores/mfrc522/ultima")
def ultima_mfrc522(

    device_id: str = None

):

    resultado = listar_leituras(

        device_id=device_id,

        sensor="MFRC522",

        limite=1

    )


    if not resultado:

        return {

            "sensor": "MFRC522",

            "leitura": None

        }


    return {

        "sensor": "MFRC522",

        "leitura": resultado[0]

    }