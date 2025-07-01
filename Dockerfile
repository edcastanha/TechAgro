FROM python:3.12-slim-bookworm

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Define variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.poetry/bin:$PATH"

# Instala dependências do sistema necessárias para compilar algumas bibliotecas Python
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \ 
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry de forma mais robusta
# Usaremos o script oficial de instalação do Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python -

# Adiciona o Poetry ao PATH (garante que esteja acessível)
ENV PATH="/usr/local/bin:$PATH"

# Copia os arquivos de dependências (pyproject.toml e poetry.lock)
COPY pyproject.toml poetry.lock /app/

# Configura o Poetry para não criar virtualenvs dentro do container
RUN poetry config virtualenvs.create false

# Instala as dependências do projeto usando Poetry
# --no-root: Não instala o pacote raiz (seu projeto) como uma dependência.
# Isso garante que as dependências do `pyproject.toml` sejam instaladas diretamente no ambiente do container.
RUN poetry install --no-root

# Copia o restante do código da aplicação
COPY . /app/

# O comando de execução (será sobrescrito pelo docker-compose)
CMD ["python", "techagro/manage.py", "runserver", "0.0.0.0:8000"]