# Roteiro do Vídeo — Pet & Gatô

**Equipe:** Ana Baldivia (RA 2840482423002), Alexandre Carvalho (RA 2840482423027), Julia Roberta (RA 2840482423020), Lídia Rocha (RA 2840482423022)
**Link do vídeo (não listado):** <https://drive.google.com/file/d/1zOwMfqF6Gi2bNpcTindYnaEg0x8BrNE0/view?usp=drivesdk>
**Duração final:** 10:30

## 1. Planejamento dos blocos
| Bloco | Tempo | Quem fala | O que aparece na tela |
|---|---|---|---|
| 1 · Abertura | 0:00–0:30 | Lídia | Capa do projeto com logo, título (Pet & Gatô) e nomes/RAs da equipe |
| 2 · Problema e cliente | 0:30–1:30 | Ana | Contexto do tema sugerido (clínica veterinária), dores do controle manual e perfil dos usuários (Recepção e Veterinário) |
| 3 · Demonstração (deploy público) | 1:30–5:10 | Alexandre | Navegação na URL pública (`https://pet-e-gato.web.app/`): perfis, cadastro tutor/pet, agendamento + vacina (21 dias), internação + plantão, dashboard e alertas da Sprint 4 |
| 4 · Engenharia: rastreabilidade | 5:10–7:00 | Alexandre | US-04/US-09 no backlog → DER/Modelagem → PR com revisão de código → Suíte Pytest (30 testes) rodando verde no GitHub Actions |
| 5 · Processo ágil | 7:00–9:10 | Lídia e Julia | Evolução planejado × entregue (Sprints 1 a 4), atas de retrospectiva aplicadas, board Kanban e rodízio de papéis |
| 6 · Depoimentos individuais | 9:10–10:10 | Todos | Cada integrante (15s cada) destacando o principal aprendizado prático |
| Fechamento | 10:10–10:30 | Ana | Tela final com URL do deploy, repositório no GitHub (`anabldv/clinica_veterinaria`) e stack tecnológica |

## 2. Requisitos mínimos na demonstração (bloco 3)
| Requisito mínimo | Momento do vídeo | Como aparece |
|---|---|---|
| Autenticação com 2+ perfis | 1:40 | Alternância entre perfis `Recepcao` e `Veterinario` (`X-Perfil`), exibindo o bloqueio (HTTP 403) quando a recepção tenta editar um prontuário |
| Regra de negócio não trivial (caso normal + borda) | 2:25 | Tentativa de agendar vacina com intervalo menor que 21 dias (HTTP 400), conflito de horário no mesmo veterinário (HTTP 409) e bloqueio de segunda evolução no mesmo turno de plantão |
| Consulta agregada (relatório/dashboard) | 3:55 | Tela de Dashboard (`GET /dashboard`) exibindo indicadores consolidados de tutores, animais, agendamentos e internações ativas estratificadas por gravidade |
| Validações em interface e banco | 2:05 | Validação no formulário SPA e via Pydantic impedindo datas retroativas, CPFs duplicados e campos obrigatórios vazios (HTTP 400 / 422) |
| 6+ entidades com N:N | 5:35 | Exibição no Bloco 4 da modelagem conectando Tutores, Animais, Usuários, Agendamentos, Vacinas, Internações e Evoluções de Plantão |
| Deploy público (URL visível) | Todo o bloco 3 | Barra de endereços do navegador exibindo `https://pet-e-gato.web.app/` durante toda a demonstração |
| Repositório com README | 10:15 | Página inicial do repositório `github.com/anabldv/clinica_veterinaria` com README estruturado |

## 3. História rastreada (bloco 4)
**História escolhida:** US-04 / US-09 — Atualização de prontuários com controle de vacinação e restrição de acesso por perfil (Veterinário vs. Recepção)

| Etapa | Artefato mostrado | Link |
|---|---|---|
| Requisito | Histórias #4 e #9 com critérios de aceite de intervalo vacinal (21 dias) e bloqueio de perfil | `docs/backlog.md` |
| Modelo | Modelagem relacional das entidades Prontuário, Vacina, Animal e Usuário | `docs/der.png` |
| Código | Pull Request da Sprint 3/4 com revisão de código sobre cabeçalho `X-Perfil` e regras de turno | `github.com/anabldv/clinica_veterinaria/pulls` |
| Teste | Casos CT18, CT24, CT25 e execução da bateria final de 30 testes aprovados no GitHub Actions | `docs/E8 - Sprint 4/evidencias_teste.md` |

**Decisão técnica justificada:** Implementamos validadores customizados no Pydantic (`@field_validator`) e injeção de dependências no FastAPI para validar datas e cabeçalhos (`X-Perfil`) antes da camada de persistência, pois garantiria integridade clínica imediata e respostas HTTP semânticas (`400`, `403`, `409`) tanto para a interface SPA quanto para integrações externas.

## 4. Evidências de processo ágil (bloco 5)
| Evidência | Sprint | Artefato mostrado na tela |
|---|---|---|
| Planejado × entregue por sprint | 1–4 | S1: 100% (10 testes) · S2: 100% (14 testes) · S3: 100% (22 testes) · S4: 100% entregue (#16, #17, #18 e SPA integrados, 30 testes) |
| Retrospectiva com ação aplicada | 2 → 3 → 4 | Ata da Sprint 2 (conflitos de merge) gerou política de branches limpas na Sprint 3; Ata da Sprint 3 gerou conexão completa da SPA e 30 testes E2E na Sprint 4 |
| Mudança de escopo negociada | 1 → 3 | Replanejamento da História #4 (controle de perfil) da Sprint 1 para a Sprint 3, negociado com a PO para priorizar o cadastro base primeiro |
| PR com revisão relevante | 3–4 | Revisão cruzada entre QA, Dados e Backend nos PRs de Dashboard e integração SPA garantindo contratos OpenAPI/Swagger |
| Rodízio de papéis | 1–4 | Tabela de responsabilidades nas entregas (Ana: PO/Frontend, Alexandre: Qualidade/CI, Julia: Dados/Backend, Lídia: Scrum Master/Backend/Docs) |

## 5. Depoimentos (bloco 6)
| Integrante | Papéis exercidos | Conceito aprendido na prática | Evidência citada | O que faria diferente |
|---|---|---|---|---|
| Ana Baldivia | PO (S1–S4), Frontend SPA | Alinhar critérios de aceite claros evita retrabalho na integração entre telas e API | Replanejamento da História #4 e integração final da SPA | Definir todos os contratos OpenAPI antes de iniciar a codificação |
| Alexandre Carvalho | Qualidade / QA (S1–S4) | Testes defensivos e automação no CI impedem regressões a cada novo Pull Request | Suíte final com 30
