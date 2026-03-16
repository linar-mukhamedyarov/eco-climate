import uvicorn
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT
import json
import logging # Logs
from config import settings  # config file
from database import db # work with db

# Logs
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
        db.add_data(
            room_id=int(topic.split("/")[-1]),
            temperature=float(json.loads(payload)["temperature"]),
            humidity=float(json.loads(payload)["humidity"]),
            co2=int(json.loads(payload)["co2"])
            )
    except:
        logger.error("Cannot add data", exc_info=True)


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
        db.close_db() # close db
