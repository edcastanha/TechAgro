# ADRs (Architecture Decision Records)


## ADR 001: Escolha do Framework Backend

**Título:** Escolha do Framework Backend - Django e Django REST Framework

**Status:** Aceito

**Contexto:** O projeto necessita de um backend robusto, escalável e com rápida prototipagem para gerenciar atendimentos agrícolas, envolvendo dados de usuários, propriedades e geolocalização. É preciso suportar tanto APIs para aplicativos móveis quanto interfaces web de administração.

**Decisão:** Utilizar Python com o Django Framework para a camada ORM e lógica de negócio, e o Django REST Framework (DRF) para a criação das APIs RESTful.

**Justificativa:**

**Django:** Oferece um ecossistema completo ("baterias inclusas"), ORM robusto, sistema de administração integrado, segurança e escalabilidade comprovadas. Facilita a modelagem de dados complexos e a integração com PostgreSQL.

**Django REST Framework:** É a ferramenta padrão para criar APIs RESTful em Django, fornecendo serializadores, autenticação, permissões e views que aceleram o desenvolvimento e garantem a conformidade com os princípios REST.

**Python:** Linguagem de programação amplamente utilizada, com vasta comunidade e bibliotecas, facilitando o desenvolvimento e manutenção.

**Consequências:**

**Positivas:** Rápido desenvolvimento de APIs, segurança nativa do Django, escalabilidade, fácil manutenção, grande comunidade de suporte.

**Negativas:** Curva de aprendizado inicial para quem não conhece Django/DRF, maior tamanho de aplicação em comparação a frameworks mais "leves".Ótimo! Com essas informações, temos um panorama muito mais claro do sistema. A divisão de usuários e as funcionalidades específicas para cada um são cruciais para o design do backend.

---

### Resumo das Novas Informações

* **Herança de Usuários:** Todos os usuários herdarão de uma classe `Pessoa` base, que conterá dados comuns de uma pessoa brasileira. Isso é uma excelente prática para reutilização de código e padronização.
* **Detalhes do Atendimento:** Teremos um formulário base com:
    * Dados da propriedade e do responsável.
    * Campos para tipo de atividade.
    * Horários (implica check-in/check-out).
    * Anotações.
    * Atividade de retorno.
* **Acesso e Integração:**
    * **App Mobile:** Agente Agrícola, Produtor, Escritório.
    * **Web/Dashboard:** Administradores.
* **Tipos de Usuários e Funcionalidades:**
    * **Administradores:** Gerenciam e visualizam todos os dados.
    * **Agente de Escritório:** Cadastra, edita e desativa produtores, propriedades e técnicos; cria atividades e edita agendas.
    * **Produtor Rural:** Visualiza suas propriedades, atendimentos realizados e agendados.
    * **Técnico Agrícola:** Organiza agendamentos, realiza check-in/check-out com atividades, notas e retorno, e registra **geolocalização em cada etapa** (check-in, início atendimento, anotações, check-out).

---

### Panorama Geral da Solução

Com base nessas informações, o sistema que vamos construir terá as seguintes características principais:

1.  **Modelagem de Dados:** Começaremos definindo modelos claros para `Pessoa`, `Produtor`, `Propriedade`, `AgenteTecnico` (o Técnico Agrícola), `AgenteEscritorio`, `Atendimento` e `Atividade` (dentro do atendimento). A herança da classe `Pessoa` será fundamental aqui.
2.  **Autenticação e Autorização:** Implementaremos um sistema robusto de autenticação e permissões usando o Django REST Framework para garantir que cada tipo de usuário acesse apenas as funcionalidades e dados permitidos.
3.  **APIs RESTful:** Expor os dados e funcionalidades através de APIs RESTful, que serão consumidas pelos aplicativos mobile e pela interface web.
4.  **Gerenciamento de Atendimentos:** Um módulo central para agendamento, check-in/check-out e registro detalhado das atividades, incluindo a crucial coleta de geolocalização em diferentes momentos.
5.  **Banco de Dados PostgreSQL:** Utilizaremos o PostgreSQL para armazenar todos os dados, aproveitando suas capacidades para dados espaciais (geométricos) se necessário para a geolocalização.

---

Agora que temos uma compreensão mais aprofundada, vamos para a primeira parte prática: as **ADRs (Architecture Decision Records)**. As ADRs são documentos curtos que registram uma decisão arquitetural importante, o contexto em que ela foi tomada, as opções consideradas e as consequências. Elas são excelentes para documentar o porquê de certas escolhas serem feitas, ajudando na comunicação e no entendimento do projeto a longo prazo.

---

### 1. ADRs (Architecture Decision Records)

Vamos documentar algumas das decisões arquiteturais iniciais mais importantes.

#### ADR 001: Escolha do Framework Backend

* **Título:** Escolha do Framework Backend - Django e Django REST Framework
* **Status:** Aceito
* **Contexto:** O projeto necessita de um backend robusto, escalável e com rápida prototipagem para gerenciar atendimentos agrícolas, envolvendo dados de usuários, propriedades e geolocalização. É preciso suportar tanto APIs para aplicativos móveis quanto interfaces web de administração.
* **Decisão:** Utilizar Python com o **Django Framework** para a camada ORM e lógica de negócio, e o **Django REST Framework (DRF)** para a criação das APIs RESTful.
* **Justificativa:**
    * **Django:** Oferece um ecossistema completo ("baterias inclusas"), ORM robusto, sistema de administração integrado, segurança e escalabilidade comprovadas. Facilita a modelagem de dados complexos e a integração com PostgreSQL.
    * **Django REST Framework:** É a ferramenta padrão para criar APIs RESTful em Django, fornecendo serializadores, autenticação, permissões e views que aceleram o desenvolvimento e garantem a conformidade com os princípios REST.
    * **Python:** Linguagem de programação amplamente utilizada, com vasta comunidade e bibliotecas, facilitando o desenvolvimento e manutenção.
* **Consequências:**
    * **Positivas:** Rápido desenvolvimento de APIs, segurança nativa do Django, escalabilidade, fácil manutenção, grande comunidade de suporte.
    * **Negativas:** Curva de aprendizado inicial para quem não conhece Django/DRF, maior tamanho de aplicação em comparação a frameworks mais "leves".

#### ADR 002: Escolha do Banco de Dados

* **Título:** Escolha do Banco de Dados - PostgreSQL
* **Status:** Aceito
* **Contexto:** O sistema precisa armazenar dados relacionais como usuários, propriedades e atendimentos, e especificamente dados de geolocalização para as visitas dos técnicos agrícolas. A integridade dos dados e a capacidade de realizar consultas espaciais são cruciais.
* **Decisão:** Utilizar **PostgreSQL** como o banco de dados principal.
* **Justificativa:**
    * **Robustez e Confiabilidade:** PostgreSQL é um dos sistemas de gerenciamento de banco de dados relacionais mais avançados e confiáveis.
    * **Suporte a Dados Geoespaciais (PostGIS):** Com a extensão PostGIS, o PostgreSQL oferece recursos poderosos para armazenamento, indexação e consulta de dados geográficos, o que é essencial para as informações de geolocalização.
    * **Integração com Django:** O Django possui excelente suporte para PostgreSQL e para o GeoDjango (extensão do Django para dados geográficos que se integra com PostGIS).
    * **Flexibilidade:** Permite modelar dados complexos e suporta operações ACID.
* **Consequências:**
    * **Positivas:** Capacidade de lidar com geolocalização de forma eficiente, alta performance, escalabilidade, integridade dos dados, ecossistema maduro.
    * **Negativas:** Requer um pouco mais de configuração inicial para PostGIS em comparação com um banco de dados simples, mas o ganho justifica o esforço.

#### ADR 003: Estrutura de Usuários com Herança

* **Título:** Estrutura de Usuários com Herança da Classe Pessoa
* **Status:** Aceito
* **Contexto:** O sistema terá múltiplos tipos de usuários (Administrador, Agente de Escritório, Produtor Rural, Técnico Agrícola), todos com atributos comuns de pessoa (nome, CPF, contato etc.), mas também com funcionalidades e atributos específicos.
* **Decisão:** Criar uma classe base `Pessoa` abstrata (ou um modelo concreto que sirva como base para outros modelos com relacionamento OneToOne) para conter os atributos comuns, e então estender ou vincular essa classe aos modelos específicos de usuário.
* **Justificativa:**
    * **Reutilização de Código:** Evita a duplicação de campos e lógica para dados pessoais em cada modelo de usuário.
    * **Padronização:** Garante que todos os usuários tenham um conjunto consistente de informações básicas.
    * **Facilidade de Manutenção:** Alterações nos dados básicos de pessoa precisam ser feitas em apenas um local.
    * **Flexibilidade:** Permite adicionar campos específicos para cada tipo de usuário sem impactar os demais.
* **Consequências:**
    * **Positivas:** Código mais limpo e organizado, menor chance de erros, fácil escalabilidade para novos tipos de usuários, manutenção simplificada.
    * **Negativas:** Requer um entendimento de herança de modelos no Django, o que pode adicionar uma pequena complexidade inicial na modelagem.

---

A seguir, criaremos os Diagramas C4 Model do projeto para termos uma visão arquitetural clara, e depois partiremos para os modelos das classes no Django.

Você gostaria de adicionar alguma ADR ou tem alguma dúvida sobre as que definimos?