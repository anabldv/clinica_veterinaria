# Ata de Retrospectiva — Sprint 4 — Pet & Gatô

**Data:** 30/10/2026  
**Presentes:** Ana Baldivia (2840482423002) — Alexandre Carvalho (2840482423027) — Julia Roberta (2840482423020) — Lídia Rocha (2840482423022)

## 1. Ações da retrospectiva anterior — foram aplicadas?
| Ação decidida | Aplicada? | Evidência/comentário |
|---|---|---|
| Conectar o frontend (HTML/JS) aos endpoints de internações, plantão e dashboard | Sim | Interface web totalmente integrada aos módulos do FastAPI. |
| Padronizar o ambiente virtual e Git na equipe | Sim | Processo de setup validado nos computadores de todos os integrantes. |
| Ampliar cenários de teste E2E com fluxo completo | Sim | Suíte elevada para 30 testes automatizados validados no CI. |

## 2. O que funcionou bem
- Integração ponta a ponta bem-sucedida entre o frontend estático e as rotas avançadas do FastAPI.
- Estabilidade total da suíte de testes com 30 casos validados sem regressões.
- Divisão clara de papéis e cumprimento rigoroso do escopo do MVP.

## 3. O que não funcionou
- Ajustes iniciais de CORS e cabeçalhos de requisição assíncrona entre a SPA e a API local.
- Pequenos gargalos na sincronização de horários UTC vs fuso local nos disparos simulados.

## 4. Ações para a próxima sprint
| Ação | Responsável |
|---|---|
| Padronizar o uso de variáveis de ambiente desde o início do projeto | Toda a equipe |
| Automatizar o empacotamento completo via containers Docker | Lídia Rocha |
