# Ata de Retrospectiva — Sprint 4 — Pet & Gatô

**Data:** 30/11/2026  
**Presentes:** Ana Baldivia (2840482423002) — Alexandre Carvalho (2840482423027) — Julia Roberta (2840482423020) — Lídia Rocha (2840482423022)

---

## 1. Ações da retrospectiva anterior — foram aplicadas?
| Ação decidida | Aplicada? | Evidência/comentário |
|---|---|---|
| Conectar o frontend (HTML/JS) aos endpoints de internações, plantão e dashboard | Sim | Interface web totalmente integrada aos módulos do FastAPI. |
| Padronizar o ambiente virtual e Git na equipe | Sim | Processo de setup validado nos computadores de todos os integrantes. |
| Ampliar cenários de teste E2E com fluxo completo | Sim | Suíte final elevada para 30 testes automatizados validados no CI. |

---

## 2. O que funcionou bem
- **Entrega completa do MVP:** Cumprimento de 100% dos requisitos estipulados no Termo de Aceite e no Backlog (Must, Should e Could).
- **Estabilidade da suíte de testes:** Atingimento de 30 testes automatizados validados com 100% de aprovação na integração contínua (GitHub Actions) sem regressões.
- **Sincronia da equipe:** Alinhamento exemplar entre os papéis de PO, Dados, Backend, Frontend e QA ao longo das 4 sprints.

---

## 3. O que não funcionou
- Curva de aprendizado na modelagem de restrições relacionais complexas entre o Oracle e os validadores do Pydantic.
- Implementação de tópicos pontuais `Could` do arquivo Backlog

---

## 4. Ações para a próxima etapa / Sprint

| Ação | Responsável |
| :--- | :--- |
| **Padronizar variáveis de ambiente e arquivos `.env` logo na Sprint 1** | Toda a equipe |
| **Utilização rigorosa de especificações OpenAPI/Swagger acopladas a validações estritas de esquema para assegurar que alterações no backend não quebrem contratos com o frontend** | Toda a equipe |
