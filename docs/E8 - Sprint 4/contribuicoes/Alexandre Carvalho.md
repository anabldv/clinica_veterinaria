# Relatório Individual de Contribuição — Sprint 4 — Alexandre Carvalho (RA 2840482423027)

**Papel nesta sprint:** Qualidade

## 1. O que fiz
| Item | PR/commit | Status |
|---|---|---|
| Desenvolvimento e validação dos casos de teste CT27 a CT30 (`test_sprint4.py`) | PR da Sprint 4 | Concluído |
| Validação de regressão da suíte completa de testes da API (30 testes no Pytest) | Pipeline CI | Concluído |
| Acompanhamento, verificação e aprovação do workflow de integração contínua (GitHub Actions) | PR #32 | Concluído |

## 2. Rituais que participei
- [x] Dailies/weeklies
- [x] Sprint Review
- [x] Retrospectiva

## 3. PRs de colegas que revisei
| PR | Autor | Comentário resumido |
|---|---|---|
| #31 | Lídia Rocha | Revisão da lógica de disparo de lembretes automáticos de consultas. |

## 4. Dificuldades e o que aprendi
- **Dificuldades:** Ajustes finos nos mocks temporais para simular inatividade de tutores superior a 1 ano sem interferir nos demais testes da suíte.
- **O que aprendi:** Técnicas avançadas de teste de rotinas baseadas em tempo (*time mocking*) e estratégias para assegurar cobertura estrita de regressão em microsserviços.
