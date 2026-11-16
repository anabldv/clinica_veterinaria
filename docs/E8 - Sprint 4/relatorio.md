# Relatório de Entrega — Sprint 4 — Pet & Gatô

**Período:** 19/10/2026 a 30/10/2026  
**Sprint Review:** 30/10/2026  

## 1. Planejado vs. Entregue

| História / Requisito (E2) | Planejada para esta sprint? | Entregue? | Observação |
| :--- | :---: | :---: | :--- |
| **#16 Alerta de Inatividade do Tutor (Check-up Anual)** | Sim | Sim | Implementação de lógica temporal de verificação de última visita ao pet (limite de 365 dias) com disparo de notificações simuladas para check-up periódico. |
| **#17 Observações Adicionais para Tutores** | Sim | Sim | Criação de campos e endpoints dedicados para inclusão, edição e remoção de notas dinâmicas e observações comportamentais/relevantes vinculadas ao cadastro do tutor. |
| **#18 Lembretes Automáticos de Consultas (E-mail/SMS)** | Sim | Sim | Módulo de automação para envio de lembretes baseados na data/hora do agendamento, com suporte a canal de comunicação configurável. |
| **Integração Completa Frontend SPA x Backend API REST** | Sim | Sim | Conexão assíncrona das telas do frontend (HTML/JS puro) com os endpoints do FastAPI (agendamentos, plantão, internações, prontuários e dashboard). |

## 2. Incremento funcional demonstrável

Módulo final de **Relacionamento com o Cliente, Alertas Preventivos e Automação de Comunicação**, integrando-se de forma fluida à interface web (*Single Page Application*) e à suíte de persistência da API REST em FastAPI. 

O sistema conta com o monitoramento automático de inatividade de tutores para campanhas de check-up preventivo anual, o gerenciamento de observações complementares e a automação de disparos de lembretes de consultas. A interface frontend consome integralmente as rotas do backend, oferecendo uma experiência unificada para os perfis de `Recepcao` e `Veterinario`.

* **Vídeo de demonstração:** 

**Passo a passo para reproduzir localmente:**
1. Acessar a pasta do backend: `cd backend`
2. Ativar o ambiente virtual: `.\.venv\Scripts\Activate.ps1`
3. Instalar as dependências: `pip install -r requirements.txt`
4. Executar os testes automatizados da suíte completa: `python -m pytest -v`
5. Iniciar o servidor da API: `python -m uvicorn app.main:app --reload`

## 3. Backlog atualizado

**Board:** Ao final desta sprint, todas as histórias previstas para o ciclo (*Could* e finalização de integrações *Must/Should*) foram concluídas (#16, #17, #18 e integração ponta a ponta da SPA). O projeto atinge o escopo completo estipulado no Termo de Aceite para o MVP.
