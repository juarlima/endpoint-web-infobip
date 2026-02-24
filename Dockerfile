FROM hub.furycloud.io/mercadolibre/distroless-python-dev:3.11-mini

WORKDIR /app

COPY requirements.txt ./

RUN python -m venv /app/venv \
    && /app/venv/bin/pip install --no-cache-dir --prefer-binary -r requirements.txt

COPY . .
