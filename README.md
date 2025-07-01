# TechAgro

API para Gestão de Produtores Rurais — Desafio Brain Agriculture

## Visão Geral
Esta aplicação fornece uma API REST para cadastro e gestão de produtores rurais, propriedades, safras e culturas, com validações de negócio, dashboard de dados agregados e documentação automática.

## Tecnologias
- Python 3.11+
- Django 5
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- drf-spectacular (OpenAPI/Swagger)

## Como rodar o projeto

### 1. Clone o repositório
```bash
git clone <seu-repo>
cd TechAgro
```

### 2. Configure as variáveis de ambiente
Copie o arquivo `.env.example` para `.env` e ajuste se necessário:
```bash
cp .env.example .env
```

### 3. Suba com Docker
```bash
docker-compose up --build
```
A API estará disponível em `http://localhost:8000/v1/api/`

### 4. Acesse a documentação
- Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

### 5. Acesso online (Fly.io)

A API está disponível publicamente em:
- Redoc: [https://techagro.fly.dev/redoc/](https://techagro.fly.dev/redoc/)
- Swagger: [https://techagro.fly.dev/swagger/](https://techagro.fly.dev/swagger/)
- Endpoint base: [https://techagro.fly.dev/v1/api/](https://techagro.fly.dev/v1/api/)

> **Atenção:** O primeiro acesso pode levar até 10 segundos para responder, pois o pod pode estar em cold start (inicialização automática na nuvem).

## Endpoints principais
- `/v1/api/produtores/` — CRUD de produtores
- `/v1/api/propriedades/` — CRUD de propriedades
- `/v1/api/safras/` — CRUD de safras
- `/v1/api/atividades/` — CRUD de culturas plantadas
- `/v1/api/dashboard/` — Dados agregados para gráficos

## Regras de Negócio
- Validação de CPF/CNPJ
- Soma das áreas agricultável + vegetação não pode exceder área total
- Relacionamentos: produtor pode ter várias propriedades, propriedade pode ter várias safras/culturas

## Testes

O projeto utiliza `pytest` e `pytest-django` para testes automatizados.

### Executando os testes

```bash
pytest
```

### Gerando relatório de cobertura

```bash
pytest --cov=techagro --cov-report=term-missing
```

> **Dica:** Os testes devem cobrir as principais regras de negócio, validações e endpoints da API.

## Observabilidade
Logs e monitoramento podem ser incrementados conforme necessidade.

## Deploy
Pronto para deploy em qualquer nuvem (exemplo: Fly.io, Heroku, etc). Basta configurar as variáveis de ambiente.

## Autor
Edson Bezerra

---
Projeto para avaliação técnica Brain Agriculture.
