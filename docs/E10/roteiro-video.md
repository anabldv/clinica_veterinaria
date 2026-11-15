# Roteiro de Vídeo — Pet & Gatô

**Equipe:** Ana Baldivia (RA 2840482423002) — Alexandre Carvalho (RA 2840482423027) — Julia Roberta (RA 2840482423020) — Lídia Rocha (RA 2840482423022)  
**Link do vídeo (não listado):** `[link a inserir]`  
**Duração final:** 10:15 (estimada entre 8 e 12 min)

## 1. Planejamento dos blocos
| Bloco | Tempo | Quem fala | O que aparece na tela |
|---|---|---|---|
| 1 · Abertura | 0:00–0:25 | Lídia | Capa institucional com o nome do projeto e os RAs da equipe |
| 2 · Problema e cliente | 0:25–1:20 | Ana | Contextualização do desafio proposto pela disciplina (gestão hospitalar veterinária) e os gargalos de controle em clínicas tradicionais |
| 3 · Demonstração (deploy público) | 1:20–4:30 | Alexandre narra, Julia navega | Tela do navegador com a URL pública do deploy (`https://pet-e-gato.web.app/`), demonstrando login por perfis, agendamentos, vacinação e dashboard |
| 4 · Engenharia: rastreabilidade | 4:30–6:20 | Alexandre | Exibição do backlog, modelagem de dados, Pull Request no GitHub e pipeline de CI executando o Pytest |
| 5 · Processo ágil | 6:20–8:40 | Lídia e Julia | Gráficos de planejado × entregue das sprints 1 a 3, atas de retrospectiva e Kanban |
| 6 · Depoimentos individuais | 8:40–9:55 | Todos | Câmera aberta de cada integrante relatando os aprendizados |
| Fechamento | 9:55–10:15 | Ana | Tela final com link do deploy, repositório GitHub e stack tecnológica |

## 2. Requisitos mínimos na demonstração (bloco 3)
| Requisito mínimo | Momento do vídeo | Como aparece |
|---|---|---|
| Autenticação com 2+ perfis | 1:35 | Demonstração de acesso alternando entre os papéis de Recepção e Veterinário (via cabeçalho `X-Perfil`), com bloqueio de rotas sensíveis |
| Regra de negócio não trivial (caso normal + borda) | 2:20 | Tentativa de agendamento de vacina com intervalo inferior a 21 dias da última dose (retornando erro HTTP 400) e conflito de horário no mesmo veterinário (HTTP 409) |
| Consulta agregada (relatório/dashboard) | 3:15 | Acesso à rota de Dashboard (`GET /dashboard`) exibindo a contagem consolidada de tutores, animais, agendamentos e internações ativas estratificadas por gravidade |
| Validações em interface e banco | 2:05 | Validações Pydantic no FastAPI impedindo datas retroativas e campos obrigatórios ausentes |
| 6+ entidades com N:N | 4:45 | Exibição do modelo relacional conectando tutores, animais, agendamentos, vacinas, internações e evoluções de plantão |
| Deploy público (URL visível) | Todo o bloco 3 | URL `https://pet-e-gato.web.app/` ativa na barra de endereços do navegador |
| Repositório com README | 10:05 | Repositório público `anabldv/clinica_veterinaria` com documentação e instruções de execução |

## 3. História rastreada (bloco 4)
**História escolhida:** US-04 / Regras de Prontuário e Restrição de Acesso por Perfil (Sprint 3)

| Etapa | Artefato mostrado | Link |
|---|---|---|
| Requisito | Backlog com critérios de aceite para perfis de Recepção versus Veterinário | `docs/backlog.md` |
| Modelo | Modelagem relacional das tabelas de Prontuário, Evolução e Perfis | `docs/der.png` |
| Código | Pull Request #22 (revisão de rotas e headers de controle de acesso) | `github.com/anabldv/clinica_veterinaria` |
| Teste | Suíte de testes automatizados (`test_sprint3.py`) com cenários de bloqueio de perfil no CI | `tests/test_sprint3.py` |

**Decisão técnica justificada:** Optamos por realizar a validação de perfis através de interceptadores e injeção de dependências no FastAPI associados a cabeçalhos customizados (`X-Perfil`), porque garante o desacoplamento inicial da camada de autenticação pesada enquanto consolida as regras restritivas do MVP clínico.

## 4. Evidências de processo ágil (bloco 5)
| Evidência | Sprint | Artefato mostrado na tela |
|---|---|---|
| Planejado × entregue por sprint | S1, S2, S3 (S4 em andamento) | S1: 100% entregue · S2: 100% entregue (14 testes) · S3: 100% entregue (22 testes) |
| Retrospectiva com ação aplicada | S2 → S3 | Ata da Sprint 2 com foco em mitigar conflitos de merge e padronizar branches aplicadas na Sprint 3 |
| Mudança de escopo negociada | S1 | Replanejamento da História #4 de controle de acesso por perfil da Sprint 1 para a Sprint 3 |
| PR com revisão relevante | S3 | Pull Request de integração das métricas do Dashboard validado cruzadamente pela equipe |
| Rodízio de papéis | S1–S3 | Matriz de papéis rotativos (Ana como PO, Alexandre em QA, Julia em Dados, Lídia como Scrum Master) |

## 5. Depoimentos (bloco 6)
| Integrante | Papéis exercidos | Conceito aprendido na prática | Evidência citada | O que faria diferente |
|---|---|---|---|---|
| Ana Baldivia | Product Owner / Dev Backend | Clareza na definição de critérios de aceite para evitar retrabalho no código | Replanejamento da História #4 entre a Sprint 1 e 3 | Detalhar os contratos de API antes de codificar |
| Alexandre Carvalho | Responsável por Qualidade (QA) | Importância da automação de testes defensivos para mitigar quebras no pipeline de CI | Suíte `test_sprint3.py` cobrindo cenários de borda | Automatizar testes de regressão desde o primeiro dia |
| Julia Roberta | Responsável por Dados / Backend | Rigor na integridade relacional de chaves e restrições de datas em Python/Pydantic | Modelagem das regras de vacinação de 21 dias e plantões | Mapear o banco relacional completo mais cedo no projeto |
| Lídia Rocha | Scrum Master / Docs / Backend | O impacto do acompanhamento diário do board Kanban e versionamento limpo | Resolução de conflitos de merge entre branches na Sprint 2 | Estabelecer um fluxo de PRs menores e mais frequentes |

## 6. Checagem antes do envio
- [x] Sem senhas, tokens, `.env` ou dados pessoais reais na tela
- [x] Autorização de imagem de quem aparece e da coordenação/proposta acadêmica
- [x] Link testado em janela anônima (`https://pet-e-gato.web.app/`)
- [x] Ficha da mostra em `docs/mostra-virtual.md` + capa + 3 capturas enviadas

