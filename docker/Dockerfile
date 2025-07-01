# Utiliza a imagem oficial do Python 3.12
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /src

# Define a variável de ambiente PYTHONPATH
ENV PYTHONPATH=/src \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copia o entrypoint customizado
COPY ./entrypoint.sh ./
RUN chmod +x ./entrypoint.sh

# Copia o arquivo de requisitos
COPY ./src/requirements.txt ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Instala o cliente do PostgreSQL para usar pg_isready no entrypoint
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client

# Copia o restante do código para o container
COPY ./src ./


# Expõe a porta padrão do FastAPI
EXPOSE 8000

# Comando para iniciar o servidor FastAPI
ENTRYPOINT ["./entrypoint.sh"]