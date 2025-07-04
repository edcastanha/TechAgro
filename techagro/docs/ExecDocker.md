# Execução do projeto via Docker e Docker Compose

### 1. Clone o repositório
```bash
git clone https://github.com/edcastanha/TechAgro
cd TechAgro
```

## Executando o Projeto

### 2. Configure as variáveis de ambiente
Copie o arquivo `.env.example` para `.env` e ajuste se necessário:
```bash
cp .env.example .env
```

### Via Docker
```bash
docker-compose up --build
```

## A API estará disponível em `http://localhost:7000/v1/api/`

[REDOC](http://localhost:7000/v1/api/redoc/) e
[SWAGGER](http://localhost:7000/v1/api/swagger/) para documentação automática.