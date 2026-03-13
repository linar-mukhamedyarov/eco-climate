from fastapi_mqtt import MQTTConfig
import uvicorn

mqtt_config = MQTTConfig(host="localhost", port=1883)
uvicorn_config = uvicorn.Config("main:app", port=8080, log_level="info", reload=True)
