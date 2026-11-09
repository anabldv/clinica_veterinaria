# Termo de Aceite do Cliente — Pet & Gatô

**Cliente/PO:** Ana Baldivia, Product Owner (Representando a Direção Clínica) <br>
**Data:** 10/11/2026

## 1. Escopo avaliado (comparado ao Termo de Aceite do Projeto — E2b)
| Funcionalidade aceita na E2b | Entregue? | Observação do cliente |
|---|---|---|
| 1. Cadastro de animal vinculado a tutor único | Sim | Vínculo validado corretamente; sistema bloqueia pet sem tutor associado. |
| 2. Cadastro de tutor com dados completos (CPF, contato) | Sim | — |
| 3. Segurança dos perfis (Recepção vs. Veterinário) | Sim | Testado e aprovado. Restrições de acesso (ex: edição de prontuários) funcionam perfeitamente para o perfil adequado. |
| 4. Atualização e agendamento de vacinas | Sim | O bloqueio de intervalo inferior a 21 dias (regra clínica) funcionou conforme o esperado. |
| 5. Gestão de agendamentos diários com verificação de conflito | Sim | Bloqueio de conflitos de horário no mesmo veterinário atuou corretamente (erro 409). |
| 6. Relatório/Dashboard de internações | Sim | Resumo consolidado em tempo real por nível de gravidade está excelente e rápido. |
| 7. Registro de atendimento clínico e plantão | Sim | Regra limitando a uma única evolução por animal no mesmo turno foi confirmada. |
| 8. Consulta de histórico clínico | Sim | Ficha clínica consolida bem o histórico de evoluções. |
| 9. Sistema eficiente e online | Sim | Publicação da API atendeu ao critério de disponibilidade contínua. |

## 2. Ressalvas / pendências
- O envio automático de lembretes de vacinação aos tutores via WhatsApp/E-mail (item *Could* do backlog) foi sugerido pela diretoria, mas confirmado como escopo para a próxima iteração, não bloqueando a entrega atual.
- A exportação dos dados do Dashboard de internações para PDF (para fins de auditoria da clínica) ficará como melhoria futura.

## 3. Parecer
[x] Aceito com ressalvas (listadas acima, não bloqueantes)

## 4. Assinatura
- Cliente/PO: Ana Baldivia (assinatura em anexo, aprovação formal registrada via plataforma de gestão do projeto em 10/11/2026)
