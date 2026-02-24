FROM hub.furycloud.io/mercadolibre/distroless-python-dev:3.11-mini

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

COPY . .
