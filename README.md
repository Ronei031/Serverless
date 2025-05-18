# 📦 Serverless Application - CRUD de Usuários com Integrações AWS

Este projeto é uma aplicação **Serverless** desenvolvida com foco em capacitação utilizando diversos serviços AWS. A aplicação implementa um CRUD completo de usuários.

---

## 🚀 Funcionalidades

- ✅ **CRUD de Usuários**
  - Criar, listar, editar e excluir usuários
  - Validação de contratos nas requisições
  - Endpoints expostos via API Gateway

- 🔐 **Autenticação com Amazon Cognito**
  - Registro e login de usuários via Cognito
  - Proteção de rotas com validação de tokens

- 📩 **Fila SQS e Auditoria**
  - Toda ação relevante escreve uma mensagem na fila SQS
  - Consumer Lambda da fila salva as mensagens na tabela de auditoria (`AuditoriaUsuarios`)

- 📣 **Evento SNS e Tabela de Usuários Teste**
  - Ao criar um novo usuário, é publicado um evento no tópico SNS
  - Subscriber Lambda consome esse evento e salva os dados na tabela `UsuariosTeste`

- ☁️ **Armazenamento e Infraestrutura**
  - DynamoDB usado para persistência em três tabelas:
    - `Usuarios`
    - `AuditoriaUsuarios`
    - `UsuariosTeste`
  - Bucket S3 utilizado para armazenar os arquivos da aplicação
  - Parâmetros sensíveis armazenados no AWS Systems Manager (SSM) para evitar exposição

- 📊 **Monitoramento e Logs**
  - Integração com Amazon CloudWatch para monitoramento de logs e falhas
  - Observabilidade centralizada por função Lambda

---

## 🛠️ Tecnologias e Serviços Utilizados

- [x] AWS Lambda
- [x] AWS API Gateway
- [x] AWS Cognito
- [x] AWS SQS
- [x] AWS SNS
- [x] AWS DynamoDB
- [x] AWS S3
- [x] AWS Systems Manager (SSM Parameter Store)
- [x] AWS CloudWatch
- [x] Serverless Framework

---

## 📁 Estrutura de Pastas

```plaintext
.serverless/               # Artefatos gerados pelo Serverless Framework
functions/
├── functions.yml          # Definição das funções Lambda
providers/
├── provider.yml           # Configurações de provider (AWS, região, runtime)
resources/
├── resources.yml          # Criação de recursos AWS (filas, tópicos, tabelas)
services/
├── auditoria_usuarios/
│   └── auditoria.py       # Consumer da SQS que grava na tabela de auditoria
├── usuarios/
│   ├── usuarios.py        # Funções CRUD dos usuários
│   └── usuarios_topico.py # Consumer do SNS que grava na tabela UsuariosTeste
utils/
├── response.py            # Helper de formatação de resposta
.gitignore
handler.py                 # Arquivo principal de roteamento das funções
serverless.yml             # Arquivo principal de configuração Serverless
README.md                  # Documentação do projeto

---

## 🧪 Endpoints

| Método | Rota                 | Descrição              | Autenticação |
|--------|----------------------|------------------------|--------------|
| GET    | `/usuarios`          | Lista todos os usuários | ✅ |
| GET    | `/usuarios/{id}`     | Busca usuário por ID    | ✅ |
| POST   | `/usuarios`          | Cria um novo usuário    | ✅ |
| PUT    | `/usuarios/{id}`     | Atualiza um usuário     | ✅ |
| DELETE | `/usuarios/{id}`     | Remove um usuário       | ✅ |

---

## 🧰 Deploy

Para realizar o deploy:

sls deploy --stage dev

🔒 Segurança
Todas as variáveis sensíveis (ARNs, segredos) são armazenadas no AWS Systems Manager (SSM)

Endpoints protegidos por autenticação via Cognito (Bearer Token JWT), exceto o de criar usuário, que foi mantido sem autenticação, para cenários de testes.

📌 Observações
A função de criação de usuário publica automaticamente um evento em um tópico SNS.

Esse evento é consumido por outra Lambda que replica o usuário em uma tabela separada UsuariosTeste.

Todas as ações CRUD disparam mensagens para a fila SQS para fins de auditoria.

O consumo da SQS salva os dados na tabela AuditoriaUsuarios.

📞 Contato
Caso tenha dúvidas ou sugestões, sinta-se à vontade para abrir uma issue ou enviar um pull request!


