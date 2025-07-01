#!/bin/bash
set -e

# Aguarda o PostgreSQL iniciar completamente
until pg_isready -h db -U "$POSTGRES_USER"; do
  echo "Aguardando PostgreSQL iniciar..."
  sleep 1
done

echo "PostgreSQL iniciado. Verificando o banco de dados '$POSTGRES_DB'..."

# Tenta criar o banco de dados APENAS SE ELE NÃO EXISTIR
# A opção -c 'EXISTS' garante que o comando não falhe se o DB já existir
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    CREATE DATABASE "$POSTGRES_DB";
EOSQL

echo "Banco de dados '$POSTGRES_DB' criado ou já existe."