# Manual do Usuário — Pet & Gatô

**Acesso ao sistema:** <https://pet-e-gato.web.app/>

## Para Recepção

### Como cadastrar um tutor e vincular seus animais
1. Acesse o sistema com suas credenciais de perfil **Recepção**.
2. No menu principal, abra a aba **Tutores** e clique em **Novo Tutor**.
3. Preencha nome completo, CPF, telefone, e-mail e observações, e clique em **Salvar**. O sistema bloqueia automaticamente cadastros com CPF já existente.
   [screenshot: tela de cadastro de tutor]
4. Em seguida, acesse a aba **Animais**, clique em **Novo Animal**, selecione o tutor recém-cadastrado e informe nome, espécie, raça e sexo do pet.
5. Ao salvar, o vínculo fica disponível imediatamente para agendamentos e consultas.
   [screenshot: tela de cadastro de animal vinculado ao tutor]

### Como agendar ou cancelar uma consulta/vacinação
1. Acesse a aba **Agendamentos** no menu superior e clique em **Novo Agendamento**.
2. Selecione o tutor, o animal, o veterinário responsável, a data/hora futura e o tipo de serviço (consulta ou vacinação).
3. O sistema valida automaticamente conflitos de horário para o mesmo veterinário e exige um intervalo mínimo de **21 dias** entre aplicações de vacinas.
   [screenshot: formulário de agendamento]
4. Para cancelar um atendimento, localize o registro na listagem de agendamentos (filtrando por veterinário ou status) e clique em **Cancelar**.

---

## Para Veterinários

### Como registrar um prontuário clínico e aplicar vacinas
1. Acesse o sistema com suas credenciais de perfil **Veterinário** (apenas veterinários possuem permissão de escrita clínica).
2. Abra a ficha do paciente na aba **Prontuários** e clique em **Novo Atendimento**.
3. Informe o seu **CRMV**, o peso atual do animal (deve ser maior que zero), a queixa principal, anamnese, diagnóstico e receita.
4. Caso uma vacina seja aplicada no atendimento, preencha o nome da vacina, lote e data da próxima dose para atualizar o histórico de imunização do pet.
   [screenshot: tela de preenchimento de prontuário clínico]

### Como gerenciar internações e registrar evoluções de plantão
1. Para internar um paciente, acesse a aba **Internações**, clique em **Nova Internação**, selecione o animal, informe seu CRMV, o motivo e o nível de gravidade (**Baixa**, **Médio**, **Alta** ou **Crítica**).
2. O sistema impede que um animal já internado receba uma segunda internação ativa simultaneamente.
   [screenshot: tela de gestão de internações e níveis de gravidade]
3. Para registrar o acompanhamento durante o turno, acesse a aba **Plantão**, selecione o paciente internado e insira a evolução clínica (permitido um registro por turno **Diurno** ou **Noturno**).
4. Para dar alta ou atualizar o quadro clínico, abra os detalhes da internação e altere o status para **Alta Médica** ou **Em Observação**.
   [screenshot: tela de evolução de plantão e atualização de status]

### Como acompanhar o painel geral (Dashboard)
1. Acesse **Dashboard** no menu principal.
2. O painel exibe em tempo real o total de tutores, animais cadastrados, agendamentos e internações ativas agrupadas por nível de gravidade.
   [screenshot: painel geral (Dashboard) com indicadores em tempo real]

---

## Perguntas frequentes

**Por que não consigo abrir ou editar um prontuário clínico?**
Por segurança e conformidade clínica, apenas usuários autenticados com perfil **Veterinário** podem criar prontuários ou registrar evoluções de plantão. Usuários de **Recepção** têm acesso apenas a cadastros e agendamentos.

**Tentei agendar uma vacina para um pet e o sistema bloqueou, o que fazer?**
O sistema aplica uma trava de segurança clínica que exige um intervalo mínimo de **21 dias** entre doses de vacina para o mesmo animal. Verifique o histórico de vacinação do pet antes de escolher a nova data.

**Não consigo cadastrar um animal sem antes cadastrar o tutor?**
Não. Para manter a integridade referencial dos dados, todo animal precisa estar obrigatoriamente vinculado a um tutor previamente cadastrado no sistema.

**Como saber se a API e o banco de dados estão online no plantão noturno?**
O sistema opera em regime **24/7** e possui monitoramento contínuo através do endpoint `/health`, que verifica em tempo real a conexão com o banco de dados e identifica automaticamente o turno vigente (Diurno das 07h às 19h ou Noturno das 19h às 07h).
