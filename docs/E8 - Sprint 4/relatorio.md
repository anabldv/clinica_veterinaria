# Relatório de Entrega — Sprint 4 — Pet & Gatô

---

**Período:** 19/10/2026 a 30/10/2026  
**Sprint Review:** 30/10/2026, com o professor Lucas B. F.

---

## 1. Planejado vs. entregue
| História (E2) | Planejada para esta sprint? | Entregue? | Observação |
|---|---|---|---|
| #16 Alerta de inatividade do tutor (check-up anual) | Sim | Sim | Lógica temporal implementada para verificar última visita ao pet (limite de 365 dias). |
| #17 Observações adicionais para tutores | Sim | Sim | Criação de campos e endpoints para inclusão, edição e remoção de notas dinâmicas no cadastro do tutor. |
| #18 Lembretes automáticos de consultas (e-mail/SMS) | Sim | Sim | Módulo de automação para envio de lembretes baseados na data/hora do agendamento. |
| Integração SPA Frontend x Backend API REST | Sim | Sim | Conexão assíncrona das telas do frontend em HTML/JS com os endpoints do FastAPI. |

---

## 2. Incremento funcional demonstrável
O sistema conta com o monitoramento automático de inatividade de tutores para campanhas de check-up preventivo anual, o gerenciamento de observações complementares e a automação de disparos de lembretes de consultas. A interface frontend consome integralmente as rotas do backend, oferecendo uma experiência unificada para os perfis de `Recepcao` e `Veterinario`.

* **Vídeo de demonstração:**  

**Passo a passo para reproduzir localmente:**
1. Acessar a pasta do backend: `cd backend`
2. Ativar o ambiente virtual: `.\.venv\Scripts\Activate.ps1`
3. Instalar as dependências: `pip install -r requirements.txt`
4. Executar os testes automatizados: `python -m pytest -v`
5. Iniciar o servidor da API: `python -m uvicorn app.main:app --reload`
6. Acessar a documentação Swagger interativa em: `http://127.0.0.1:8000/docs`

---

## 3. Backlog atualizado
**Board:** Ao final desta sprint, todas as histórias previstas para o ciclo (*Could* e finalização de integrações *Must/Should*) foram concluídas (#16, #17, #18 e integração ponta a ponta da SPA). O projeto atinge o escopo completo estipulado no Termo de Aceite para o MVP.

---

## 4. Evidências de teste
Testes unitários, de integração e de ponta a ponta cobrindo os fluxos felizes e validações críticas das funcionalidades finais do sistema (alertas de inatividade anual, gerenciamento de observações de tutores, lembretes automáticos e integração SPA), com retornos HTTP validados (`200`, `201`, `400` e `404`). Ao todo, foram executados **30 testes automatizados** (22 herdados das Sprints 1, 2 e 3 + 8 novos da Sprint 4), todos **100% aprovados** tanto localmente quanto na esteira de integração contínua (GitHub Actions). Detalhe completo em: `docs/E8 - Sprint 4/evidencias_teste.md`

---

## 5. Retrospectiva e contribuição individual
- **Ata de retrospectiva:** `docs/E8 - Sprint 4/retrospectiva.md`
- **Relatórios individuais de contribuição da equipe (nome + RA):** localizados na pasta `docs/contribuicoes/`

## 6. Riscos/impedimentos para a próxima sprint
Com a entrega do MVP completo validada em ambiente de testes e documentada, o ciclo de desenvolvimento acadêmico do semestre é encerrado com sucesso. Como recomendações para futuras evoluções de mercado, aponta-se a migração definitiva da camada em memória para um pool de conexões persistentes em produção com Oracle corporativo em nuvem e a expansão do frontend para um framework reativo moderno (como React ou Vue).
