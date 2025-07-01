# Casos de Teste da API

Este documento contém exemplos de requisições e respostas para todos os endpoints da API.


# Produtores
1. Criar Produtor
POST /produtores/
Headers:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Request:

{
  "documento": "12345678901",
  "nome": "João da Silva"
}
Response (201 Created):

{
  "id": 1,
  "documento": "12345678901",
  "nome": "João da Silva",
  "propriedades": [],
  "created_at": "2024-03-14T10:00:00",
  "updated_at": "2024-03-14T10:00:00"
}
2. Listar Produtores
GET /produtores/
Headers:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Response (200 OK):

[
  {
    "id": 1,
    "documento": "12345678901",
    "nome": "João da Silva",
    "propriedades": [
      {
        "id": 1,
        "nome": "Fazenda São João",
        "cidade": "São Paulo",
        "estado": "SP",
        "area_total": 1000.0,
        "area_agricultavel": 700.0,
        "area_vegetacao": 300.0,
        "produtor_id": 1,
        "culturas": [
          {
            "id": 1,
            "nome": "Soja",
            "ano_safra": 2024,
            "area": 500.0,
            "propriedade_id": 1,
            "created_at": "2024-03-14T10:00:00",
            "updated_at": "2024-03-14T10:00:00"
          }
        ],
        "created_at": "2024-03-14T10:00:00",
        "updated_at": "2024-03-14T10:00:00"
      }
    ],
    "created_at": "2024-03-14T10:00:00",
    "updated_at": "2024-03-14T10:00:00"
  }
]
3. Obter Produtor
GET /produtores/{produtor_id}
Headers:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Response (200 OK):

{
  "id": 1,
  "documento": "12345678901",
  "nome": "João da Silva",
  "propriedades": [
    {
      "id": 1,
      "nome": "Fazenda São João",
      "cidade": "São Paulo",
      "estado": "SP",
      "area_total": 1000.0,
      "area_agricultavel": 700.0,
      "area_vegetacao": 300.0,
      "produtor_id": 1,
      "culturas": [
        {
          "id": 1,
          "nome": "Soja",
          "ano_safra": 2024,
          "area": 500.0,
          "propriedade_id": 1,
          "created_at": "2024-03-14T10:00:00",
          "updated_at": "2024-03-14T10:00:00"
        }
      ],
      "created_at": "2024-03-14T10:00:00",
      "updated_at": "2024-03-14T10:00:00"
    }
  ],
  "created_at": "2024-03-14T10:00:00",
  "updated_at": "2024-03-14T10:00:00"
}
4. Atualizar Produtor
PUT /produtores/{produtor_id}
Headers:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Request:

{
  "documento": "12345678901",
  "nome": "João da Silva Atualizado"
}
Response (200 OK):

{
  "id": 1,
  "documento": "12345678901",
  "nome": "João da Silva Atualizado",
  "propriedades": [
    {
      "id": 1,
      "nome": "Fazenda São João",
      "cidade": "São Paulo",
      "estado": "SP",
      "area_total": 1000.0,
      "area_agricultavel": 700.0,
      "area_vegetacao": 300.0,
      "produtor_id": 1,
      "culturas": [
        {
          "id": 1,
          "nome": "Soja",
          "ano_safra": 2024,
          "area": 500.0,
          "propriedade_id": 1,
          "created_at": "2024-03-14T10:00:00",
          "updated_at": "2024-03-14T10:00:00"
        }
      ],
      "created_at": "2024-03-14T10:00:00",
      "updated_at": "2024-03-14T10:00:00"
    }
  ],
  "created_at": "2024-03-14T10:00:00",
  "updated_at": "2024-03-14T10:00:00"
}
5. Deletar Produtor
DELETE /produtores/{produtor_id}
Headers:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Response (200 OK):

{
  "message": "Produtor deletado com sucesso"
}


# Propriedades
1. Adicionar Propriedade
POST /produtores/{produtor_id}/propriedades
Headers:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Request:

{
  "nome": "Fazenda São João",
  "cidade": "São Paulo",
  "estado": "SP",
  "area_total": 1000.0,
  "area_agricultavel": 700.0,
  "area_vegetacao": 300.0
}
Response (201 Created):

{
  "id": 1,
  "nome": "Fazenda São João",
  "cidade": "São Paulo",
  "estado": "SP",
  "area_total": 1000.0,
  "area_agricultavel": 700.0,
  "area_vegetacao": 300.0,
  "produtor_id": 1,
  "culturas": [],
  "created_at": "2024-03-14T10:00:00",
  "updated_at": "2024-03-14T10:00:00"
}

# Culturas
1. Adicionar Cultura
POST /produtores/{produtor_id}/propriedades/{propriedade_id}/culturas
Headers:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Request:

{
  "nome": "Soja",
  "ano_safra": 2024,
  "area": 500.0
}
Response (201 Created):

{
  "id": 1,
  "nome": "Soja",
  "ano_safra": 2024,
  "area": 500.0,
  "propriedade_id": 1,
  "created_at": "2024-03-14T10:00:00",
  "updated_at": "2024-03-14T10:00:00"
}


# Dashboard
1. Obter Resumo
GET /dashboard/resumo
Headers:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Response (200 OK):

{
  "total_propriedades": 1,
  "area_total_hectares": 1000.0,
  "distribuicao_estados": {
    "SP": 1
  },
  "distribuicao_culturas": {
    "Soja": 500.0
  },
  "distribuicao_uso_solo": {
    "area_agricultavel": 700.0,
    "area_vegetacao": 300.0
  }
}

# Health Check
1. Verificar Status
GET /health
Response (200 OK):

{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-03-14T10:00:00"
}

# Códigos de Erro
1. Bad Request (400)
{
  "detail": "Documento deve ter 11 dígitos"
}
2. Unauthorized (401)
{
  "detail": "Could not validate credentials"
}
3. Forbidden (403)
{
  "detail": "Not enough permissions"
}
4. Not Found (404)
{
  "detail": "Produtor não encontrado"
}
5. Unprocessable Entity (422)
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email address",
      "type": "value_error.email"
    }
  ]
}
6. Internal Server Error (500)
{
  "detail": "Internal server error"
}


# Autenticação
1. Registrar Usuário
POST /auth/register
Request:

{
  "email": "teste@exemplo.com",
  "password": "senha123"
}
Response (200 OK):

{
  "id": 1,
  "email": "teste@exemplo.com",
  "is_active": true,
  "created_at": "2024-03-14T10:00:00"
}
2. Login
POST /auth/token
Request (form-data):

username: teste@exemplo.com
password: senha123
Response (200 OK):

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
3. Obter Usuário Atual
GET /auth/me
Headers:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Response (200 OK):

{
  "id": 1,
  "email": "teste@exemplo.com",
  "is_active": true,
  "created_at": "2024-03-14T10:00:00"
}
