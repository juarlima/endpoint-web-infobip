FROM hub.furycloud.io/mercadolibre/distroless-python-dev:3.11-mini

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
