# Evidências de Teste — Sprint 1 — Pet & Gatô

| ID | Caso de teste | Tipo | Resultado | Evidência |
|---|---|---|---|---|
| CT01 | Cadastro de tutor com CPF já existente na base | Integração |  | Sistema identifica o CPF duplicado e impede o cadastro do tutor, respeitando a constraint UNIQUE definida no banco de dados |
| CT02 | Criação de usuário com senha fora do padrão de segurança | Integração |  | Banco recusa a senha que não atende aos critérios mínimos de segurança e apresenta os requisitos necessários para uma senha forte |
| ----- | CPF válido no cadastro do tutor | Integração |  | Sistema permite o cadastro quando o CPF do tutor informado atende ao formato e aos critérios de validação definidos |
| ----- | E-mail válido no cadastro do tutor  | Integração |  | Sistema aceita o endereço de e-mail quando informado em formato válido |
| ----- | Cadastro de tutor com todos os campos obrigatórios preenchidos | Integração |  | Sistema permite a conclusão do cadastro do tutor quando todos os campos obrigatórios são preenchidos corretamente, armazenando os dados na base |
| ----- | Cadastro de animal vinculado a um tutor existente | Unitário + Integração |  | Sistema permite cadastrar o animal e associá-lo a um tutor previamente cadastrado, mantendo o relacionamento entre as entidades |
| ----- | E-mail do usuário no padrão empresarial | Unitário |  | Sistema valida o domínio do email antes de completar o login/cadastro |
| ----- | CNPJ válido no cadastro do usuário veterinário | Integração + Unitário |  | Sistema permite o cadastro do veterinário quando o CNPJ informado atende a todos os padrões de formatação |
| ----- | CPF válido no cadastro do usuário recepção | Integração + Unitário |  | Sistema permite o cadastro quando o CPF da recepção informado atende ao formato e aos critérios de validação definidos |

## Cobertura automatizada nesta sprint
[Resumo do que o CI reporta, ex.: "18 testes, 100% passando, cobertura de 62% no módulo de negócio"]
