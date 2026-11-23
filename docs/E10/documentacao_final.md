# Documentação Final — Pet & Gatô

**Deploy definitivo:** <https://pet-e-gato.web.app/>  
**Repositório:** <https://github.com/Anabe-dev/clinica_veterinaria>

## 1. Índice de artefatos do semestre
| Entrega | Documento | Link |
|---|---|---|
| E1 | Documento de Visão | [`docs/E1/documento_de_visao.md`](./docs/E1/documento_de_visao.md) |
| E2 | Backlog + <br> Termo de Aceite do Projeto | [`docs/E2/backlog.md`](./docs/E2/backlog.md) <br> [`docs/E2/termo_de_aceite_do_projeto.md`](./docs/E2/termo_de_aceite_do_projeto.md) |
| E3 | UML + <br> DER + <br> DDL | [`docs/E3/diagramas_UML.md`](./docs/E3/diagramas_UML.md) <br> [`docs/E3/DER.md`](./docs/E3/DER.md) <br> [`database/schema.sql`](./database/schema.sql) |
| E4 | README + <br> Protótipo + <br> Plano de Testes | [`README.md`](./README.md) <br> [`docs/E4/roteiro_do_prototipo_navegavel.md`](./docs/E4/roteiro_do_prototipo_navegavel.md) <br> [`docs/E4/plano_de_testes.md`](./docs/E4/plano_de_testes.md) |
| E5 <br> E6 <br> E7 <br> E8 | Relatórios de sprint | [`docs/E5 - Sprint 1/relatorio.md`](./docs/E5%20-%20Sprint%201/relatorio.md) <br> [`docs/E6 - Sprint 2/relatorio.md`](./docs/E6%20-%20Sprint%202/relatorio.md) <br> [`docs/E7 - Sprint 3/relatorio.md`](./docs/E7%20-%20Sprint%203/relatorio.md) <br> [`docs/E8 - Sprint 4/relatorio.md`](./docs/E8%20-%20Sprint%204/relatorio.md) |
| E9 | Relatório de testes + <br> Termo de Aceite do Cliente | [`docs/E9/relatorio_testes_final.md`](./docs/E9/relatorio-testes-final.md) <br> [`docs/E9/termo_aceite_cliente.md`](./docs/E9/termo-aceite-cliente.md) |

## 2. Desvios do escopo original (vs. E2b)
| Item | Mudou? | Justificativa |
|---|---|---|
| Autenticação e controle de acesso | Simplificado (cabeçalho `x-perfil` e `/login` direto) | Priorização das regras de negócio clínicas (prontuários, vacinas, internações e plantão) e integração front-end/back-end dentro do prazo das 4 sprints |
| Persistência em ambiente de CI (GitHub Actions) | Adicionado modo híbrido (`oracledb` + memória em testes) | O servidor Linux do GitHub Actions não possui instância Oracle Database local; a alternância automática permite validar os 27 testes automatizados no pipeline de CI sem alterar as queries SQL de produção |
| Hospedagem do Front-end | Definida no Firebase Hosting (`pet-e-gato.web.app`) | Garante disponibilização pública imediata da interface estática (HTML/CSS/JS) com HTTPS nativo para validação do cliente |

## 3. Arquitetura final (resumo)
Sem mudanças estruturais desde a E4: front-end em **HTML5, CSS3 e JavaScript** (hospedado no Firebase Hosting) consumindo via REST/JSON a API desenvolvida em **Python com FastAPI**, conectada ao banco de dados relacional **Oracle Database** (`oracledb`) com 8 tabelas principais (`tb_usuario`, `tb_tutor`, `tb_animal`, `tb_agendamento`, `tb_prontuario`, `tb_vacinacao`, `tb_plantao` e `tb_internacao`). Na Sprint 4 foram adicionados o middleware de **CORS**, o endpoint de monitoramento contínuo **`GET /health`** (disponibilidade 24/7) e o pipeline automatizado de testes (**Pytest + GitHub Actions**).

## 4. Como contribuir/rodar
Ver [`README.md`](./README.md) na raiz — atualizado nesta entrega com o link de deploy definitivo (<https://pet-e-gato.web.app/>), instruções de configuração do Oracle Database (`DB_USER`, `DB_PASSWORD`, `DB_DSN`) e comandos para execução da API (`uvicorn`) e da suíte de testes (`pytest`).
