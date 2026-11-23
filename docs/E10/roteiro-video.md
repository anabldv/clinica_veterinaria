# Roteiro de Apresentação — Pet & Gatô

**Equipe:** Ana Baldivia (RA 2840482423002), Alexandre Carvalho (RA 2840482423027), Julia Roberta (RA 2840482423020), Lídia Rocha (RA 2840482423022)  
**Deploy público:** <https://pet-e-gato.web.app/>  
**Repositório:** <https://github.com/Anabe-dev/clinica_veterinaria>

---

## 1. Vídeo de demonstração (3–5 min)
**Link do vídeo:** <https://drive.google.com/file/d/1zOwMfqF6Gi2bNpcTindYnaEg0x8BrNE0/view?usp=drivesdk>

| Tempo | Conteúdo | Quem narra |
|---|---|---|
| 0:00–0:35 | **Problema e público-alvo:** Contexto da clínica veterinária, gargalos das planilhas/fichas impressas e perfis operacionais (**Recepção** e **Veterinário**). | Lídia / Ana |
| 0:35–2:45 | **Demonstração do fluxo principal (Deploy público):** Navegação em `https://pet-e-gato.web.app/`: autenticação e controle de acesso por perfil (`X-Perfil`), cadastro de tutor e animal, agendamento de consultas/vacinas e gestão de internações/plantão. | Alexandre |
| 2:45–4:15 | **Diferenciais técnicos:** Validações de regras clínicas (intervalo mínimo de 21 dias entre vacinas, bloqueio de conflito de horário e evolução única por turno), consulta agregada no **Dashboard** (`GET /dashboard`), monitoramento 24/7 (`GET /health`) e suíte de **27 testes automatizados** passando no GitHub Actions. | Alexandre / Julia |
| 4:15–4:45 | **Encerramento:** Visão geral do repositório documentado, rastreabilidade e link de acesso definitivo. | Ana |

### Checklist de requisitos demonstrados no vídeo
* [x] **Autenticação com 2+ perfis:** Alternância entre `Recepcao` e `Veterinario`, mostrando o bloqueio (`HTTP 403`) quando a recepção tenta editar prontuário.
* [x] **Regras de negócio não triviais:** Bloqueio de vacina com menos de 21 dias (`HTTP 400`), conflito de agenda do veterinário (`HTTP 409`) e evolução duplicada no mesmo turno de plantão (`HTTP 409`).
* [x] **Consulta agregada:** Tela de Dashboard (`GET /dashboard`) exibindo indicadores consolidados de tutores, animais, agendamentos e internações por gravidade.
* [x] **Validações na interface e banco:** Bloqueio de CPF duplicado, datas retroativas e integridade referencial (tutor/animal inexistente retornando `HTTP 404`).

---

## 2. Pitch ao vivo (10 min + 5 min perguntas)

| Bloco | Tempo | Quem fala | Conteúdo |
|---|---|---|---|
| **1 · Abertura e Problema** | 0:00–1:30 | Lídia | Apresentação da equipe, dores do controle manual em clínicas veterinárias e proposta de valor do **Pet & Gatô**. |
| **2 · Produto e Fluxo do Usuário** | 1:30–3:30 | Ana | Demonstração ao vivo da interface SPA hospedada no Firebase (`pet-e-gato.web.app`) e jornada dos perfis Recepção e Veterinário. |
| **3 · Arquitetura e Banco de Dados** | 3:30–5:30 | Julia | Arquitetura desacoplada (SPA + FastAPI + Oracle Database com 8 tabelas relacionais) e regras de integridade referencial. |
| **4 · Engenharia, Qualidade e CI/CD** | 5:30–7:30 | Alexandre | Rastreabilidade (US-04/US-09 $\rightarrow$ `docs/E3/DER.md` $\rightarrow$ PRs $\rightarrow$ `docs/E8 - Sprint 4/evidencias_teste.md`), arquitetura híbrida para testes e pipeline GitHub Actions com **27 testes Pytest** aprovados. |
| **5 · Processo Ágil e Retrospectivas** | 7:30–9:00 | Lídia | Evolução planejado $\times$ entregue nas Sprints 1 a 4, ações aplicadas das retrospectivas (política de branches limpas) e rodízio de papéis. |
| **6 · Aprendizados e Fechamento** | 9:00–10:00 | Todos | Síntese dos aprendizados práticos de cada integrante (15s
