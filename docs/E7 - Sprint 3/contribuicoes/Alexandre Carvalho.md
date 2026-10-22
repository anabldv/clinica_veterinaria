# Relatório Individual de Contribuição — Sprint 3 — Alexandre Carvalho (RA 2840482423027)
**Papel nesta sprint:** Qualidade

---

### 1. O que fiz

| Item | PR/commit | Status |
| :--- | :--- | :--- |
| **Criação dos testes da Sprint 3 (`test_sprint3.py`)**<br>Cobri os fluxos das histórias Should (CT19 ao CT26): validações de internação, gravidade, bloqueio de pet já internado, evoluções de plantão com cabeçalho e métricas do dashboard. | `tests/test_sprint3.py` | Concluído |
| **Correção de imports e caminhos para o CI**<br>Corrigi erro de digitação no `main.py` e ajustei a importação dos caminhos no arquivo de teste para o Pytest rodar liso no GitHub Actions. | `app/main.py` / `test_sprint3.py` | Concluído |
| **Abertura de PR e validação do pipeline**<br>Sincronizei as branches, abri o PR final e garanti que os 22 testes passassem verde tanto localmente quanto no CI. | PR da Sprint 3 (`anabldv/clinica_veterinaria`) | Concluído |
| **Evidências e documentação**<br>Compilei os prints das execuções e estruturei a documentação de testes da sprint. | Docs da Sprint 3 | Concluído |

---

### 2. Rituais que participei
- **Dailies/weeklies:** Participei dos alinhamentos semanais para atualizar o status da escrita dos testes e alinhar os contratos de dados dos novos endpoints com o time.
- **Sprint Review:** Acompanhei a validação das rotas no Swagger e o fechamento do escopo entregue na sprint.
- **Retrospectiva:** Debatemos os pontos fortes e os gargalos com Git/CI para deixar o fluxo mais redondo.

---

### 3. PRs de colegas que revisei

| PR | Autor | Comentário resumido |
| :--- | :--- | :--- |
| **#21 — Endpoints de Internação** | Julia Roberta | Revisei as validações dos níveis de gravidade e o bloqueio para não duplicar internação de um pet já internado. |
| **#22 — Rotas de Plantão** | Ana Baldivia | Analisei o tratamento do header `X-Perfil` e a lógica do cálculo de turnos para barrar mais de uma evolução no mesmo plantão. |
| **#23 — Métricas do Dashboard** | Lídia Rocha | Conferi a contagem das internações ativas estratificadas por severidade e se os retornos batiam com os testes. |

---

### 4. Dificuldades e o que aprendi

* **Git e Forks:** Quebrei um pouco a cabeça para abrir o PR porque meu fork estava desatualizado em relação à `main` da equipe e o GitHub acusava que não tinha nada para comparar. Aprendi a sincronizar a branch antes e prestar atenção na branch de origem na hora de comparar.
* **Erros sutis quebrando o CI:** Tive problemas com erros simples de digitação (um `Optiona` no import e a falta de underline no `__file__`) que não davam erro no teste avulso, mas travavam todo o pipeline do GitHub Actions no Linux. Aprendi a olhar o log do runner com calma para achar logo a linha com problema.
* **Foco em testes defensivos:** Aprendi a pensar mais em como quebrar a API com dados errados (como gravidade inválida ou horário repetido) do que apenas testar se ela funciona quando tudo é enviado certo.
