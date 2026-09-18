# Evidências de Teste — Sprint 1 — Pet & Gatô

| ID | Caso de teste | Tipo | Resultado | Evidência |
|---|---|---|---|---|
| CT01 | Cadastro de tutor com CPF já existente na base |  |  | Sistema identifica o CPF duplicado e impede o cadastro do tutor, respeitando a constraint UNIQUE definida no banco de dados |
| CT02 | Criação de usuário com senha fora do padrão de segurança |  |  | Banco recusa a senha que não atende aos critérios mínimos de segurança e apresenta os requisitos necessários para uma senha forte |

## Cobertura automatizada nesta sprint
[Resumo do que o CI reporta, ex.: "18 testes, 100% passando, cobertura de 62% no módulo de negócio"]
