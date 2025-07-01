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

## 4. Estrutura Sugerida de Pastas
## Dominio principal
| core 
|-- domain
|   |-- entities
|   |-- value_objects
|   |-- repositories
|   |-- services
|   |-- exceptions
|-- application
|   |-- use_cases
|   |-- services
|-- infrastructure
|   |-- repositories
|   |-- services
|-- interfaces
|   |-- api
|       |-- controllers
|       |-- serializers
|       |-- views
|   |-- cli
|       |-- commands
|       |-- options
|-- tests
|   |-- unit
|   |-- integration
|   |-- functional
