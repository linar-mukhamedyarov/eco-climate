FROM apache/superset:latest
WORKDIR /app
USER root
RUN uv pip install --no-cache-dir psycopg2-binary
USER superset
