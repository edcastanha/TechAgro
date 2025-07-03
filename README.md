# TechAgro

## API para Gestão de Produtores Rurais


> **Aviso:** Esta API é uma prova de conceito (POC) para fins de avaliação técnica. **Todos os dados são fictícios** e não representam informações reais. **Não foi implementado nenhum mecanismo de autenticação** para facilitar o acesso e uso da API durante a avaliação, eliminando a necessidade de cadastro ou login.

## Visão Geral
Esta aplicação fornece uma API REST para cadastro e gestão de produtores rurais, propriedades, safras e culturas, com validações de negócio, dashboard de dados agregados e documentação automática.

## Tecnologias
- Python 3.11+
- Django 5
- Django REST Framework
- PostgreSQL
- Nginx (opcional, para produção)
- Docker & Docker Compose
- drf-spectacular (OpenAPI/Swagger)

## Executando o Projeto via Docker e Docker Compose
[Página sobre execução via Docker](https://edcastanha.github.io/TechAgro/ExecDocker/)
## Executando o Projeto localmente (sem Docker)
[Página sobre execução local](https://edcastanha.github.io/TechAgro/ExecLocal/)

A API estará disponível em `http://localhost:7000/v1/api/`

## Endpoints principais
|   URL   | Descrição |
|---------|-----------|
|[http://localhost:7000/v1/api/produtores/](http://localhost:7000/v1/api/produtores/) | CRUD de produtores |
|[http://localhost:7000/v1/api/propriedades/](http://localhost:7000/v1/api/propriedades/) | CRUD de propriedades |
|[http://localhost:7000/v1/api/safras/](http://localhost:7000/v1/api/safras/) | CRUD de safras |
|[http://localhost:7000/v1/api/atividades/](http://localhost:7000/v1/api/atividades/) | CRUD de culturas plantadas |
|[http://localhost:7000/v1/api/dashboard/](http://localhost:7000/v1/api/dashboard/) | Dados agregados para gráficos | 


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
[Perfil](https://www.linkedin.com/in/edsonlbfilho/)

---
Projeto para avaliação técnic.a, não é um produto finalizado. Sinta-se à vontade para contribuir ou sugerir melhorias!

