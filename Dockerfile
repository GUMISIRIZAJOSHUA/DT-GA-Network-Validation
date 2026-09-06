FROM python:3.9

RUN apt-get update && apt-get install -y --no-install-recommends iproute2 && pip install --no-cache-dir numpy matplotlib

WORKDIR /app
