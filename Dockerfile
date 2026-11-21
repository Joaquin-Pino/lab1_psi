FROM python:3.13-slim

# ffmpeg lo necesita pydub para leer formatos distintos de wav
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Se copia solo lo necesario para instalar, para aprovechar la cache de capas
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir -e ".[dev]"

COPY . .

CMD ["pytest"]
