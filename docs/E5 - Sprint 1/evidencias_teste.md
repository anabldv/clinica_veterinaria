# Evidências de Teste — Sprint 1 — Pet & Gatô

| ID | Caso de teste | Tipo | Resultado | Evidência |
|---|---|---|---|---|
| CT01 | Cadastro de tutor com CPF já existente na base | Integração |  | Sistema identifica o CPF duplicado e impede o cadastro do tutor, respeitando a constraint UNIQUE definida no banco de dados |
| CT02 | Criação de usuário com senha fora do padrão de segurança | Integração |  | Banco recusa a senha que não atende aos critérios mínimos de segurança e apresenta os requisitos necessários para uma senha forte |
| ----- | CPF válido no cadastro do tutor | Integração |  |  |
| ----- | E-mail válido no cadastro do tutor  | Integração |  |  |
| ----- | Cadastro de tutor com todos os campos obrigatórios preenchidos | Integração |  |  |
| ----- | Cadastro de animal vinculado a um tutor existente | Unitário + Integração |  |  |
| ----- | Senha do usuário no padrão empresarial | Unitário |  |  |
| ----- | CNPJ válido no cadastro do usuário veterinário | Integração + Unitário |  |  |
| ----- | CPF válido no cadastro do usuário recepção | Integração + Unitário |  |  |

## Cobertura automatizada nesta sprint
[Resumo do que o CI reporta, ex.: "18 testes, 100% passando, cobertura de 62% no módulo de negócio"]
