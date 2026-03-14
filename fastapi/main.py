import uvicorn
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT
import json
from config import settings  # config file

# Logs
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# initialisation
app = FastAPI()
mqtt = FastMQTT(config=settings.mqtt_config)  # connect to mqtt broker
mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    client.subscribe("/room/#")


@mqtt.on_message()
async def getData(client, topic, payload, qos, properties):
    try:
        logger.info(f"Temp: {json.loads(payload)["temperature"]}, CO2: {json.loads(payload)["co2"]}")
    except:
        logger.error("Cannot convert data from JSON to python dict")


# test
# @app.post("/testdata")
# async def sendData(data):
#     mqtt.publish("/room/102", payload=data)


if __name__ == "__main__":
    try:
        uvicorn.run(
            app="main:app",
            host=settings.uvicorn_host,
            port=settings.uvicorn_port,
            reload=settings.uvicorn_reload,
        )
    except:
        logger.warning(msg="Server are shuting down", exc_info=True)
    finally:
        ## Close db
        pass
