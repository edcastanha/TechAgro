# TechAgro


API para Gestão de Produtores Rurais — Desafio Brain Agriculture

> **Aviso:** Esta API é uma prova de conceito (POC) para fins de avaliação técnica. **Todos os dados são fictícios** e não representam informações reais. **Não foi implementado nenhum mecanismo de autenticação** para facilitar o acesso e uso da API durante a avaliação, eliminando a necessidade de cadastro ou login.

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
git clone https://github.com/edcastanha/TechAgro
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

### 5. Deploy para acesso online (Fly.io) - Primeiro acesso pode demorar ate 10s por start de pods

A API está disponível publicamente em:
- Redoc: [https://techagro.fly.dev/redoc/](https://techagro.fly.dev/redoc/)
- Swagger: [https://techagro.fly.dev/swagger/](https://techagro.fly.dev/swagger/)
- Endpoint base: [https://techagro.fly.dev/v1/api/](https://techagro.fly.dev/v1/api/)

> **Atenção:** O primeiro acesso pode levar até 10 segundos para responder, pois o pod pode estar em cold start (inicialização automática na nuvem).

## Como rodar o projeto localmente (sem Docker)

1. Crie e ative um ambiente virtual:

```bash
python3 -m venv .virtual
source .virtual/bin/activate
```

2. Instale o Poetry (caso não tenha):

```bash
pip install poetry
```

3. Instale as dependências do projeto:

```bash
poetry install
```

4. Configure as variáveis de ambiente:

```bash
cp .env.example .env
```

5. Execute as migrações e popule o banco com dados mock:

```bash
python techagro/manage.py migrate
python techagro/manage.py popular_mock
```

6. Rode o servidor local:

```bash
python techagro/manage.py runserver
```

Acesse a API em: http://localhost:8000/v1/api/

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

## Dados de exemplo (mock)

Para facilitar testes e demonstrações, você pode popular o banco com dados fictícios (produtores, propriedades, safras e culturas válidas) usando:

```bash
python manage.py popular_mock
```

Esse comando garante que todos os dados respeitam as regras de negócio (CPFs/CNPJs válidos, áreas consistentes, etc).

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

## Exemplos de payloads

### Criar produtor (POST /v1/api/produtores/)
```json
{
  "documento": "12345678909",
  "nome": "Produtor Exemplo"
}
```

### Resposta (201 Created)
```json
{
  "id": "<uuid>",
  "documento": "12345678909",
  "tipo_documento": "CPF",
  "nome": "Produtor Exemplo",
  "Propriedades": []
}
```

### Criar propriedade (POST /v1/api/propriedades/)
```json
{
  "produtor": "<id_produtor>",
  "nome_propriedade": "Fazenda Exemplo",
  "area_total_hectares": 100,
  "area_agricultavel_hectares": 60,
  "area_vegetacao_hectares": 40,
  "cidade": "Uberlândia",
  "estado": "MG"
}
```

### Criar safra (POST /v1/api/safras/)
```json
{
  "propriedade": "<id_propriedade>",
  "ano": 2024,
  "data_inicio": "2024-01-01",
  "data_fim": "2024-12-31"
}
```

### Criar cultura plantada (POST /v1/api/atividades/)
```json
{
  "safra": "<id_safra>",
  "nome_cultura": "Soja",
  "area_plantada_hectares": 50
}
```

### Exemplo de resposta do dashboard (GET /v1/api/dashboard/)
```json
{
  "total_fazendas": 6,
  "total_hectares": 800,
  "por_estado": [
    {"estado": "MG", "qtd": 2},
    {"estado": "SP", "qtd": 2}
  ],
  "por_cultura": [
    {"nome_cultura": "Soja", "qtd": 4},
    {"nome_cultura": "Milho", "qtd": 3}
  ],
  "uso_solo": {
    "total_agricultavel": 400,
    "total_vegetacao": 200
  }
}
```
