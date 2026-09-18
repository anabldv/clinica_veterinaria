# Relatório de Entrega — Sprint 1 — Pet & Gatô

**Período:** 12/09/2026 a 18/09/2026 <br>
**Sprint Review:** 18/09/2026, com Lucas B. F.

## 1. Planejado vs. entregue
| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #1 Cadastro tutor | Sim | Sim | -- |
| #2 Cadastro animal | Sim | Sim | -- |
| #3 Segurança de senhas | Sim | Sim | -- |
| #4 Atualização de prontuário com data de vacinação | Sim | Não | Precisa da segregação dos perfis, movida para a sprint 3 |

## 2. Incremento funcional demonstrável
[Descrição do que está rodando + link do deploy ou GIF/vídeo + como reproduzir localmente] Exemplo: Login com 2 perfis, CRUD de empresa e convênio funcionando com validação de CNPJ e datas.
Ambiente rodando localmente (deploy público só a partir da E4/E9). Vídeo de 2 min da
demonstração: `docs/sprints/sprint-1-demo.mp4`. Passo a passo para reproduzir: ver README
na raiz do repositório.

## 3. Backlog atualizado
[Print/link do board ao fim da sprint + lista do que mudou de status] Exemplo: Board: https://github.com/orgs/equipe-estagiofatec/projects/1 — ao fim da sprint, 3 cards
moveram de "A fazer" para "Concluído", 1 card (#4) ficou em "Em andamento" e foi replanejado
para a Sprint 2.

## 4. Evidências de teste
Foram realizados e documentados 8 testes de integração e 4 testes unitários para validação dessa sprint, todos passando em CI. 

Detalhe completo: [evidencias_teste.md](https://github.com/anabldv/clinica_veterinaria/blob/main/docs/E5%20-%20Sprint%201/evidencias_teste.md).

## 5. Retrospectiva e contribuição individual
- Ata de retrospectiva: [Ata](https://github.com/Anabe-dev/clinica_veterinaria/blob/main/docs/E5%20-%20Sprint%201/retrospectiva.md)
- Relatórios individuais de contribuição: [[Relatórios individuais de contribuição]](https://github.com/Anabe-dev/clinica_veterinaria/tree/main/docs/E5%20-%20Sprint%201/contribuicoes)

## 6. Riscos/impedimentos para a próxima sprint
O principal ponto identificado para as próximas sprints é a implementação das regras de controle de acesso por perfil e sua integração com as funcionalidades clínicas. A história #4 foi replanejada devido a esse ponto, é necessário garantir que funcionalidades relacionadas ao prontuário e à vacinação sejam acessíveis de acordo com o perfil do usuário, nesse caso, ao perfil do veterinário.

Além disso, a Sprint 2 deverá concentrar esforços nas funcionalidades de gestão de agendamentos, especialmente na prevenção de conflitos de horário, na visualização dos agendamentos por status e veterinário e na validação do intervalo entre doses de vacinas.
