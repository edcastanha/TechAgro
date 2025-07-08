Vamos criar um backend com python Django Framework e DFR com Postgres para gerenciar atividades de visitas de agentes técnicos agrícolas (Agente de Campo) para produtores rurais (produtores) em suas propriedades (com dados de geolocalização).

## Do Atendimento:

- Cadastro de atendimento por propriedade.

- - Vínculo de Propriedade

- - Data de atendimento

- Receberemos dados de check-in de atendimento

- - Dados de horas de chegada.

- - Inicialização de atendimento.

- - Geolocalização do técnico para atendimento.

- Atividades

- - Tipo de ações ou orientações para com o produtor

----
No backend, vamos criar um sistema que permita:
- Cadastro e gerenciamento de usuários (Agente de Campo, Produtor Rural, Administradores).
- Cadastro e gerenciamento de propriedades rurais.
- Registro de atendimentos, incluindo check-in e check-out com geolocalização.
- Registro de atividades realizadas durante os atendimentos, com possibilidade de anotações e retorno para futuras visitas.



**Tipos de Usuário:** Teremos diferentes perfis de usuário, como "Agente de Campo" e "Produtor Rural"? Se sim, eles terão acesso a funcionalidades diferentes no sistema?

**Dados do Produtor e da Propriedade:** Além do nome e geolocalização da propriedade, quais outras informações você gostaria de armazenar sobre o produtor rural e suas propriedades? (Ex: CPF/CNPJ, contato, tipo de cultura, etc.)

**Detalhes do Atendimento:** O que exatamente você espera registrar como "Tipo de ações ou orientações para com o produtor"? Seria um campo de texto livre, ou teremos tipos pré-definidos de atividades (ex: "Orientação sobre pragas", "Análise de solo", "Recomendação de insumos")?

**Check-in/Check-out:** Você mencionou "horas de chegada" e "inicialização de atendimento". Haverá também um "check-out" ou "finalização de atendimento" com registro de horas de saída? A geolocalização será registrada apenas no check-in, ou em múltiplos momentos durante o atendimento?

**Acesso e Integração:** Este backend será consumido por qual tipo de aplicação? (Ex: um aplicativo mobile para os agentes de campo, um dashboard web para a gestão?)

Todos os usuários herdarão de uma classe pessoa com dados convencionais de uma pessoa brasileira.

**Detalhes do Atendimento:** Criaremos um formulário base com os dados da propriedade e responsável e campos de tipo de atividade, horários e anotações e atividade de retorno.

**Acesso e Integração:** O Agente Agricola, Produtor, Escritório por meio App Mobile.

Ja Administradores via Web e Dashboard de monitoramento.

1 - Tipos de Usuario:

1.1 - Administradores = Gerencia e visualizadas todos os dados

1.2 - Agente de escritório = Cadastra, Edita e Desativa cadastros de produtores, propriedades e técnicos de campo, Cria atividades e edita agendas de técnicos de campo.

1.3 - Produtor Rural = Visualiza dados de usas propriedades e atendimentos realizados e agendados.

1.4 - Tecnico Agrícola - Organiza os agendamentos por datas e horários, realiza check-in na propriedade, realiza check-out com cadastro de atividades realizadas, cria notas de atendimento e retorno para próxima visita.
Enviará via api a cada 10 minutos de geolocalização em cada etapa do atendimento (check-in, início atendimento, anotações, check-out)