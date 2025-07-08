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
