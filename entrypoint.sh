#!/bin/sh
set -e

# Aguarda o banco de dados ficar disponível
until pg_isready -h db -p 5432 -U techagro_user; do
  echo "Aguardando o banco de dados..."
  sleep 2
done

# Executa o seed para criar tabelas e dados iniciais
python3 -m infrastructure.seed

# Inicia o servidor FastAPI com OpenTelemetry
exec uvicorn server:app --reload --host 0.0.0.0 --port 8000
