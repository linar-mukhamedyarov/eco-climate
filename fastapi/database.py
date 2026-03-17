import psycopg2
from config import settings
from datetime import datetime


class DbModel:
    def __init__(self):
        self.conn = psycopg2.connect(
            f"dbname={settings.db_name} user={settings.db_user} password={settings.db_password} host={settings.db_host} port={settings.db_port}"
        )
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS room_metrics (
                        time TIMESTAMPTZ NOT NULL,
                        room_id INTEGER NOT NULL,
                        temperature DOUBLE PRECISION,
                        humidity DOUBLE PRECISION,
                        co2 INTEGER NOT NULL) WITH (
                        tsdb.hypertable,
                        tsdb.orderby = 'time DESC')
                    """)
        self.conn.commit()

    def add_data(self, room_id: int, temperature: float, humidity: float, co2: int):
        self.cur.execute(f"""INSERT INTO room_metrics VALUES (
                      '{datetime.now().isoformat()}',
                      {room_id},
                      {temperature},
                      {humidity},
                      {co2})""")
        self.conn.commit()

    def close_db(self):
        self.cur.close()
        self.conn.close()

db = DbModel()