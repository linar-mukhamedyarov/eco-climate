import psycopg2
from config import settings

conn = psycopg2.connect(f"dbname={settings.db_name} user={settings.db_user} password={settings.db_password} host={settings.db_host} port={settings.db_port}")
cur = conn.cursor()

async def create_table(table_name: str):
    await cur.execute(f"""CREATE TABLE {table_name}(
                      time TIMESTAMPTZ NOT NULL,
                      temperature DOUBLE PRECISION,
                      humidity DOUBLE PRECISION)
                      """)
cur.close()
conn.close()
