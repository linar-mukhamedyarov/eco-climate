from pydantic_settings import BaseSettings
from fastapi_mqtt import MQTTConfig


# settings from .env file
class Settings(BaseSettings):
    # uvicorn settings
    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 8080
    uvicorn_reload: bool = False
    # mqtt broker settings
    mqtt_host: str = "mosquitto"
    mqtt_port: int = 1883
    # db settings
    db_url: str = ""
    db_user: str = ""
    db_password: str = ""

    # get mqtt_config
    @property
    def mqtt_config(self) -> MQTTConfig:
        return MQTTConfig(host=self.mqtt_host, port=self.mqtt_port)


settings = Settings()
