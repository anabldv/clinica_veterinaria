# Evidências de Teste — Sprint 4 — Pet & Gatô
**Projeto:** Sistema de Gestão Veterinária (Pet & Gatô)  
**Módulo:** Backend / API REST (Alertas de Inatividade, Observações de Tutores e Lembretes Automáticos)  
**Ambiente de Execução:** Python 3.11 / Python 3.13 / FastAPI / Pytest / GitHub Actions

---

## 1. Matriz de Casos de Teste (Sprint 4)

| ID | Funcionalidade | Cenário / Entrada | Resultado Esperado | Status |
| :--- | :--- | :--- | :--- | :--- |
| CT27 | Alerta de inatividade do tutor (>365 dias) | Integração / Backend | Aprovado | Retorno de aviso preventivo de check-up anual para o pet |
| CT28 | Inclusão de observações adicionais ao tutor | API REST / Pydantic | Aprovado | Status 201 Created + nota vinculada com sucesso ao ID do tutor |
| CT29 | Edição e remoção de notas do tutor | Unitário / Backend | Aprovado | Status 200 OK com texto atualizado e persistido corretamente |
| CT30 | Disparo de lembrete automático de consulta | Automação / API | Aprovado | Log de simulação de envio de e-mail/SMS registrado no sistema |

---

## 2. Evidências de Execução

### 2.1. Execução Local dos Testes Automatizados (VS Code)

<img width="780" height="311" alt="image" src="https://github.com/user-attachments/assets/0283d483-7345-4307-9e0b-a68152ff5f56" />


### 2.2. Integração Contínua (GitHub Actions — Pull Request)

<img width="1497" height="806" alt="image" src="https://github.com/user-attachments/assets/1971a586-adcb-4a20-b409-caf3d3e8cffb" />


### 2.3. Log Detalhado da Execução no Servidor de CI

27 testes executados, 100% passando (6 da Sprint 1, 8 da Sprint 2, 8 da Sprint 3 e 5 novos da Sprint 4), cobrindo regras de negócio, restrições relacionais e rotinas de notificação no Pytest, validadas localmente e no pipeline de CI (GitHub Actions).
