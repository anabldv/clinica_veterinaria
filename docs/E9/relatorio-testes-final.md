# Relatório de Testes Executados — Sistema de Gestão Veterinária (Pet & Gatô)

**Data da bateria final:** 09/11/2026<br>
**Escopo testado:** MVP do Backend / API REST englobando as Sprints 1, 2, 3 e 4 (Tutores, Animais, Agendamentos, Vacinação, Internações, Evolução de Plantão e Dashboard).

## 1. Resumo executivo
| Métrica | Valor |
|---|---|
| Total de casos de teste | 26 mapeados na matriz (CT01 a CT26) |
| Passaram | 26 (100% de aprovação técnica dos cenários) |
| Falharam | 0 na bateria final do pipeline |
| Cobertura automatizada (linhas/branches) | 22 testes automatizados executados e aprovados com sucesso no ambiente CI/CD (GitHub Actions) |

## 2. Casos de teste — visão consolidada
| ID | Área | Tipo | Resultado | Observação |
|---|---|---|---|---|
| CT01–CT10 | Cadastro de Tutores, Animais e Usuários | Unitário/integração | Passou | Casos herdados da Sprint 1 |
| CT11–CT18 | Agendamento de Consultas e Regras de Vacinação | Unitário/integração | Passou | Casos herdados da Sprint 2 |
| CT19–CT26 | Internações, Evolução de Plantão e Dashboard | Integração | Passou | Casos adicionados e validados na Sprint 3 |

## 3. Bugs encontrados nesta bateria
| # | Descrição | Severidade | Status |
|---|---|---|---|
| 1 | Conflito de regras no CT25 (Evolução de Plantão) exigiu ajuste no tratamento do cabeçalho `X-Perfil` para barrar mais de uma evolução no mesmo turno | Média | Corrigido e aprovado (Status 409 Conflict implementado) |
| 2 | O CT18 (Regra de Vacinação) falhou inicialmente ao não identificar datas retroativas corretamente devido à ausência de validadores de fuso horário | Média | Corrigido e aprovado (Status 400 Bad Request retornado para intervalo menor que 21 dias) |
| 3 | A contagem do Dashboard (CT26) não consolidava corretamente a gravidade se o pet já possuísse internações antigas desativadas | Alta | Corrigido e aprovado (Status 200 OK + indicadores em tempo real validados) |

## 4. Testes de aceitação com cliente/PO
Realizado em 09/11/2026 com a Product Owner (PO) da equipe e stakeholders da clínica veterinária. Roteiro seguido:
* Cadastro de um novo tutor e respectivo animal com dados válidos.
* Simulação de agendamento de consulta garantindo a aplicação correta da regra de bloqueio de conflitos de horário (CT12).
* Registro de uma internação com gravidade "Alta" (CT19) e validação de que o sistema bloqueia uma tentativa de internação duplicada (CT21).
* Verificação da atualização em tempo real dos dados na rota de Dashboard.
* Resultado: Aprovado para o escopo do MVP. O backend garante as validações de negócio essenciais, com retorno integral `0` (sucesso) nos logs do GitHub Actions para todos os testes submetidos.
