# Relatório Individual de Contribuição — Sprint 3 — Lídia Rocha (RA 2840482423022)

**Papel nesta sprint:** Desenvolvedora Back-end

---

## 1. O que fiz

| Item | PR/commit | Status |
| :--- | :--- | :---: |
| **Desenvolvimento das Métricas do Dashboard**<br>Implementei a lógica e os endpoints para a contagem de internações ativas estratificadas por severidade, atuando em conjunto com a Julia (que estruturou a rota da tela inicial). | PR #23 | Concluído |
| **Integração Backend e QA**<br>Trabalhei em parceria com o Alexandre para alinhar os contratos de dados do dashboard com a suíte de testes (`test_sprint3.py`), garantindo a assertividade dos retornos das métricas. | PR #23 | Concluído |
| **Apoio no troubleshooting do CI/CD**<br>Auxiliei a equipe na resolução de erros de sintaxe nos imports que estavam quebrando o pipeline do Pytest no GitHub Actions. | Commit local | Concluído |

---

## 2. Rituais que participei

- [x] Dailies/weeklies
- [x] Sprint Review
- [x] Retrospectiva

---

## 3. PRs de colegas que revisei

| PR | Autor | Comentário resumido |
| :--- | :--- | :--- |
| **#45 (ou Commit 37a9441) — Prontuários e Dashboard Geral** | Julia Roberta | Avaliei a integração das minhas métricas de internação com a rota principal do Dashboard que a Julia criou, além de revisar a aplicação das regras de restrição de perfil (Veterinário vs. Recepção) para garantir que os dados sensíveis fossem exibidos corretamente. |
| **Testes da Sprint 3 e Ajustes CI** | Alexandre Carvalho | Revisei a implementação dos casos de teste (CT19 ao CT26) aplicados aos meus endpoints, validando se as asserções cobriam cenários de erro e refletiam a nossa regra de negócios. |

---

## 4. Dificuldades e o que aprendi

- **Dificuldades:** 
  - O principal desafio foi garantir que a lógica complexa de métricas do dashboard funcionasse em perfeita harmonia com as novas restrições de acesso (perfis de Veterinário e Recepção) implementadas pela Julia. Exigiu bastante cuidado para que a agregação dos dados de internação por severidade não expusesse informações para o perfil incorreto.
  - Sincronizar o ambiente de desenvolvimento entre as branches para fechar os PRs sem conflitos, especialmente com as atualizações constantes no pipeline de testes do GitHub Actions que o Alexandre estava subindo.

- **O que aprendi:** 
  - Aprofundei meu entendimento sobre a estruturação de regras de negócio para ambientes hospitalares, compreendendo como lidar com validações dinâmicas de cabeçalho (`X-Perfil`) no FastAPI e refletir isso em rotas de consolidação de dados.
  - Desenvolvi uma visão muito mais madura sobre trabalho em equipe e integração contínua, vendo na prática como o código do PO/Dev (Julia), o meu código (Backend) e as validações automatizadas (Alexandre/QA) se conectam para formar um ecossistema seguro e funcional.
