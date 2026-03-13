import uvicorn
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
import json

# Logs
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# initialisation
mqtt_config = MQTTConfig(host="localhost", port=1883)
app = FastAPI()
mqtt = FastMQTT(config=mqtt_config)
mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    client.subscribe("/room/#")
    logger.info("Subscribed to '/room/#'")
    return


@mqtt.on_message()
async def getData(client, topic, payload, qos, properties):
    print(json.loads(payload)["temperature"], json.loads(payload)["co2"])


# test
# @app.post("/testdata")
# async def sendData(data):
#     mqtt.publish("/room/102", payload=data)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
