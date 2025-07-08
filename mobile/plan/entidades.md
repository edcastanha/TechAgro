Entidade: Usuário
Markdown

### Usuário

| Campo          | Tipo de Dados | Descrição                                    |
| :------------- | :------------ | :------------------------------------------- |
| **id_usuario** | UUID/String   | Identificador único do usuário (chave primária) |
| nome           | String        | Nome completo do usuário                     |
| email          | String        | Endereço de e-mail do usuário (único)        |
| senha_hash     | String        | Hash da senha do usuário                     |
| tipo_usuario   | Enum          | Tipo de usuário (e.g., 'agente', 'tecnico', 'administrador') |
Entidade: Pessoa
Markdown

### Pessoa

| Campo         | Tipo de Dados | Descrição                                  |
| :------------ | :------------ | :----------------------------------------- |
| **id_pessoa** | UUID/String   | Identificador único da pessoa (chave primária) |
| id_usuario    | UUID/String   | Chave estrangeira para a entidade `Usuário` (relação 1:1) |
| cpf           | String        | CPF da pessoa (único)                      |
| rg            | String        | RG da pessoa                               |
| data_nascimento | Date          | Data de nascimento da pessoa               |
| telefone      | String        | Telefone de contato da pessoa              |
| endereco      | String        | Endereço da pessoa                         |
| tipo_pessoa   | Enum          | Tipo da pessoa (e.g., 'proprietario', 'responsavel') |


## Entidade: Propriedade
### Propriedade

| Campo            | Tipo de Dados | Descrição                                    |
| :--------------- | :------------ | :------------------------------------------- |
| **id_propriedade** | UUID/String   | Identificador único da propriedade (chave primária) |
| nome_propriedade | String        | Nome da propriedade rural                    |
| latitude         | Decimal       | Latitude da localização da propriedade       |
| longitude        | Decimal       | Longitude da localização da propriedade      |
| tamanho_area     | Decimal       | Tamanho da área da propriedade (em hectares, por exemplo) |
| tipo_cultura_criacao | String      | Descrição do tipo de cultura ou criação da propriedade |
| id_proprietario  | UUID/String   | Chave estrangeira para a entidade `Pessoa` (tipo 'proprietario') |
| id_responsavel   | UUID/String   | Chave estrangeira para a entidade `Pessoa` (tipo 'responsavel', pode ser nulo se o proprietário for o responsável) |


## Entidade: Atendimento
### Atendimento

| Campo             | Tipo de Dados | Descrição                                    |
| :---------------- | :------------ | :------------------------------------------- |
| **id_atendimento** | UUID/String   | Identificador único do atendimento (chave primária) |
| id_tecnico        | UUID/String   | Chave estrangeira para a entidade `Usuário` (tipo 'tecnico') |
| id_propriedade    | UUID/String   | Chave estrangeira para a entidade `Propriedade` |
| data_agendamento  | Date          | Data agendada para o atendimento             |
| hora_agendamento  | Time          | Hora agendada para o atendimento             |
| status_atendimento | Enum          | Status do atendimento (e.g., 'agendado', 'iniciado', 'concluido', 'cancelado') |
| observacoes       | String        | Observações relevantes sobre o atendimento (opcional) |


## Entidade: CheckIn
### CheckIn

| Campo              | Tipo de Dados | Descrição                                    |
| :----------------- | :------------ | :------------------------------------------- |
| **id_checkin** | UUID/String   | Identificador único do check-in (chave primária) |
| id_atendimento     | UUID/String   | Chave estrangeira para a entidade `Atendimento` |
| id_tecnico         | UUID/String   | Chave estrangeira para a entidade `Usuário` (tipo 'tecnico') |
| latitude_inicio    | Decimal       | Latitude do local de check-in                |
| longitude_inicio   | Decimal       | Longitude do local de check-in               |
| timestamp_checkin  | DateTime      | Data e hora exatas do check-in               |


## Entidade: Deslocamento
### Deslocamento

| Campo                 | Tipo de Dados | Descrição                                    |
| :-------------------- | :------------ | :------------------------------------------- |
| **id_deslocamento** | UUID/String   | Identificador único do deslocamento (chave primária) |
| id_atendimento        | UUID/String   | Chave estrangeira para a entidade `Atendimento` |
| id_tecnico            | UUID/String   | Chave estrangeira para a entidade `Usuário` (tipo 'tecnico') |
| latitude_partida      | Decimal       | Latitude do ponto de partida do deslocamento |
| longitude_partida     | Decimal       | Longitude do ponto de partida do deslocamento |
| latitude_chegada      | Decimal       | Latitude do ponto de chegada do deslocamento (normalmente a propriedade) |
| longitude_chegada     | Decimal       | Longitude do ponto de chegada do deslocamento |
| tempo_estimado_chegada | Integer       | Tempo estimado de chegada em minutos (ou outra unidade, se preferir) |
| timestamp_registro    | DateTime      | Data e hora do registro do deslocamento      |
Essa estrutura de entidades, utilizando UUIDs para IDs e relacionamentos claros entre as tabelas através de chaves estrangeiras, segue os princípios de Clean Architecture e SOLID. 

## Entidade: CheckOut
### CheckOut

| Campo                 | Tipo de Dados | Descrição                                    |
| :-------------------- | :------------ | :------------------------------------------- |
| **id_checkout** | UUID/String   | Identificador único do check-out (chave primária) |
| id_atendimento        | UUID/String   | Chave estrangeira para a entidade `Atendimento` |
| id_tecnico            | UUID/String   | Chave estrangeira para a entidade `Usuário` (tipo 'tecnico') |
| latitude_fim          | Decimal       | Latitude do local de check-out                 |
| longitude_fim         | Decimal       | Longitude do local de check-out                |
| timestamp_checkout    | DateTime      | Data e hora exatas do check-out                |
| observacoes_final     | String        | Observações finais do técnico sobre o atendimento (opcional) |

Com a adição da entidade CheckOut, agora temos uma estrutura completa para registrar o início e o fim de cada atendimento, incluindo a geolocalização e o tempo.