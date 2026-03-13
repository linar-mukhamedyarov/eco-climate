FROM python:3.12-slim AS builder
ENV VIRTUAL_ENV="/opt/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY /app/requirements.txt .
RUN pip install -r requirements.txt

# Final stage
FROM python:3.12-slim
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv
COPY ./app /app
WORKDIR /app

CMD ["python", "main.py"]
