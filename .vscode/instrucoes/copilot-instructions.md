# Instruções para Desenvolvimento Python

Este documento define diretrizes para desenvolvimento de software Python neste projeto, garantindo aderência aos princípios SOLID, código limpo (Clean Code) e Domain-Driven Design (DDD).

---

## 1. SOLID

- **S**ingle Responsibility Principle: Cada classe/módulo deve ter uma única responsabilidade.
- **O**pen/Closed Principle: Classes devem ser abertas para extensão, mas fechadas para modificação.
- **L**iskov Substitution Principle: Subtipos devem ser substituíveis por seus tipos base.
- **I**nterface Segregation Principle: Prefira várias interfaces específicas a uma interface geral.
- **D**ependency Inversion Principle: Dependa de abstrações, não de implementações concretas.

## 2. Clean Code

- Use nomes descritivos para variáveis, funções e classes em pt-BR sem acentuação.
- Escreva funções pequenas e com uma única responsabilidade.
- Evite duplicação de código e arquivos desnecessários.
- Mantenha o código organizado e modularizado.
- Comente apenas o necessário; o código deve ser autoexplicativo.

- Prefira composição a herança quando possível.
- Escreva testes automatizados para todas as funcionalidades.

## 3. Domain-Driven Design (DDD)

- Separe o código em camadas: Domínio, Aplicação, Infraestrutura e Apresentação.
- Modele entidades, agregados, value objects e repositórios conforme o domínio.
- Use serviços de domínio para lógica que não pertence a uma entidade específica.
- Mantenha o domínio isolado de detalhes de infraestrutura.
- Utilize Ubiquitous Language: o vocabulário do código deve refletir o domínio do negócio.

## 4. Estrategia e Estrutura Sugerida de Pastas
## Framework e Dominio Puro
A estrutura de pastas do projeto deve seguir os princípios de Clean Architecture, separando claramente as
.
├── framework/                    # A pasta raiz do seu projeto Django (sua "configuração global")
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py               # Configurações base do Django
│   │   ├── dev.py                # Configurações de desenvolvimento
│   │   └── prod.py               # Configurações de produção
│   ├── urls.py                   # URLs globais do projeto Django
│   ├── wsgi.py
│   ├── asgi.py
│   └── manage.py                 # O script de gerenciamento do Django
│
├── src/                          # ONDE ESTÁ A SUA ARQUITETURA LIMPA (Domínio Puro!)
│   ├── core/                     # Camada Mais Interna: O Coração do Negócio (Domínio Puro)
│   │   ├── domain/               # Entidades, Objetos de Valor, Agregados, Exceções de Domínio
│   │   │   ├── __init__.py
│   │   │   ├── entities/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── pessoa_ou_empresa.py # Entidades: Pessoa, Empresa (com CPF/CNPJ como VOs)
│   │   │   │   ├── produtor.py        # Entidade: Produtor (associa Pessoa/Empresa)
│   │   │   │   ├── propriedade_rural.py # Entidade: PropriedadeRural (associada a Produtor)
│   │   │   │   ├── safra.py           # Entidade: Safra (associada a PropriedadeRural)
│   │   │   │   └── cultura_plantada.py  # Entidade: CulturaPlantada (associada a Safra)
│   │   │   ├── value_objects/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── documentos.py    # Objetos de Valor: CPF, CNPJ (com lógica de validação)
│   │   │   │   ├── areas.py         # Objeto de Valor: MedidaArea (hectares, validação)
│   │   │   │   └── localizacao.py   # Objeto de Valor: Cidade, Estado
│   │   │   └── exceptions.py      # Exceções de Domínio (ex: AreaInvalidaError)
│   │   │
│   │   └── ports/                # Interfaces (Contratos) que a Infraestrutura deve implementar
│   │       ├── __init__.py
│   │       ├── produtor_repository.py      # Interface: IProdutorRepository
│   │       ├── propriedade_repository.py   # Interface: IPropriedadeRuralRepository
│   │       ├── safra_repository.py
│   │       └── cultura_repository.py
│   │
│   ├── application/              # Camada de Aplicação: Orquestração dos Casos de Uso
│   │   ├── __init__.py
│   │   ├── dtos/                 # Data Transfer Objects (DTOs para entrada/saída de casos de uso)
│   │   │   ├── __init__.py
│   │   │   ├── produtor_dtos.py
│   │   │   ├── propriedade_dtos.py
│   │   │   ├── safra_dtos.py
│   │   │   └── cultura_dtos.py
│   │   └── use_cases/            # Implementação dos Casos de Uso (lógica de orquestração)
│   │       ├── __init__.py
│   │       ├── cadastrar_produtor_rural.py  # Use Case: CadastrarProdutorRuralUseCase
│   │       ├── atualizar_propriedade.py     # Use Case: AtualizarPropriedadeRuralUseCase
│   │       ├── adicionar_cultura_safra.py   # Use Case: AdicionarCulturaASafraUseCase
│   │       └── buscar_produtor.py           # Use Case: BuscarProdutorUseCase
│   │
│   ├── infrastructure/           # Camada de Infraestrutura: Adaptadores para tecnologias externas
│   │   ├── __init__.py
│   │   ├── database/             # App Django: `produtor_rural_infra` (interação com o DB)
│   │   │   ├── __init__.py
│   │   │   ├── apps.py           # Configuração da app Django
│   │   │   ├── models.py         # **Modelos Django ORM** (mapeamento para o banco de dados)
│   │   │   ├── admin.py          # Configurações do Admin Django
│   │   │   ├── migrations/
│   │   │   │   └── ...
│   │   │   └── repositories/     # **Implementações Concretas dos Repositórios** (usando Django ORM)
│   │   │       ├── __init__.py
│   │   │       ├── django_produtor_repository.py    # Implementa IProdutorRepository
│   │   │       ├── django_propriedade_repository.py  # Implementa IPropriedadeRuralRepository
│   │   │       └── ...
│   │   ├── services/             # Adaptadores para serviços externos (ex: e-mail, APIs de terceiros)
│   │   │   ├── __init__.py
│   │   │   └── email_service.py
│   │   └── security/             # Implementações de segurança (autenticação, hashing, etc.)
│   │       ├── __init__.py
│   │       └── auth_backend.py
│   │
│   └── presentation/             # Camada de Apresentação: Adaptadores para interfaces de usuário
│       ├── __init__.py
│       ├── api/                  # App Django: `produtor_rural_api` (API RESTful com DRF)
│       │   ├── __init__.py
│       │   ├── apps.py           # Configuração da app Django
│       │   ├── urls.py           # **URLs da API** (usando roteadores DRF)
│       │   ├── views/            # **DRF ViewSets / APIViews** (recebem requisições e chamam Use Cases)
│       │   │   ├── __init__.py
│       │   │   └── produtor_views.py # ViewSet para Produtores
│       │   ├── serializers/      # **DRF Serializers** (validação e serialização de dados)
│       │   │   ├── __init__.py
│       │   │   ├── produtor_serializers.py
│       │   │   ├── propriedade_serializers.py
│       │   │   ├── safra_serializers.py
│       │   │   └── cultura_serializers.py
│       │   └── middlewares.py    # Middlewares específicos da API
│       └── web/                  # App Django: `produtor_rural_web` (Interface Web tradicional)
│           ├── __init__.py
│           ├── apps.py
│           ├── urls.py
│           ├── views.py          # **Django Views** (baseadas em função ou classe para HTML)
│           ├── forms.py          # **Django Forms** (para formulários HTML)
│           └── templates/        # Templates HTML
│               └── produtores/
│                   └── ...
│
├── tests/                        # Testes (unitários, integração, E2E)
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── .env                          # Variáveis de ambiente
├── .gitignore
├── pyproject.toml                # Gerenciamento de dependências (Poetry)
├── Dockerfile                    # Definição da imagem Docker
├── docker-compose.yml            # Orquestração de containers
└── README.md