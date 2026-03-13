import uvicorn
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT
import json
import sys

# configs
sys.path.append("../configs/")
from config import mqtt_config, uvicorn_config

# Logs
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# initialisation
app = FastAPI()
mqtt = FastMQTT(config=mqtt_config)  # connect to mqtt broker
mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    client.subscribe("/room/#")
    logger.info("Subscribed to '/room/#'")
    return


@mqtt.on_message()
async def getData(client, topic, payload, qos, properties):
    try:
        print(json.loads(payload)["temperature"], json.loads(payload)["co2"])
    except:
        logger.error("Cannot convert data from JSON to python dict")


# test
# @app.post("/testdata")
# async def sendData(data):
#     mqtt.publish("/room/102", payload=data)


if __name__ == "__main__":
    server = uvicorn.Server(uvicorn_config)
    try:
        server.run()
    except:
        logger.warning(msg="Server are shuting down", exc_info=True)
    finally:
        ## Close db
        pass
