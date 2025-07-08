# Executando o Projeto localmente (sem Docker)

### Crie e ative um ambiente virtual:

```bash
python3 -m venv .virtual
source .virtual/bin/activate
```
### Instale o Poetry (caso não tenha):

```bash
pip install poetry
```
### Instale as dependências do projeto:

```bash
poetry install
```
### Configure as variáveis de ambiente:
```bash
cp .env.example .env
```
### Execute as migrações e popule o banco com dados mock:
```bash
python techagro/manage.py migrate
```
### Dados de exemplo (mock)

Para facilitar testes e demonstrações, você pode popular o banco com dados fictícios (produtores, propriedades, safras e culturas válidas) usando:

```bash
python manage.py popular_mock
```
Esse comando garante que todos os dados respeitam as regras de negócio (CPFs/CNPJs válidos, áreas consistentes, etc).

### Rode o servidor local:

```bash
python techagro/manage.py runserver
```

## A API estará disponível em `http://localhost:7000/v1/api/`

[REDOC](http://localhost:7000/v1/api/redoc/) e
[SWAGGER](http://localhost:7000/v1/api/swagger/) para documentação automática.