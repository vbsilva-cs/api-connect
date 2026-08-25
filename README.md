# API Connect

API REST para gerenciamento de usuários, desenvolvida em Python com Flask. O projeto implementa um MVP com operações de criação, consulta, atualização e remoção lógica, utilizando um arquivo JSON como mecanismo de persistência local.

## Funcionalidades

- Verificação de disponibilidade da API.
- Cadastro, listagem e consulta de usuários por ID.
- Atualização e remoção lógica de usuários.
- Validação de nome, e-mail, campos obrigatórios e tipo de conteúdo.
- Detecção de e-mails duplicados.

## Tecnologias

- Python 3.13.5
- Flask 3.1.3
- `pytest` para os testes automatizados e `requests` para o smoke test HTTP
- JSON para persistência provisória

## Estrutura do projeto

```text
api-connect/
├── controllers/
│   └── validacao.py       # Validações das entradas da API
├── models/
│   └── dados.json         # Dados persistidos localmente
├── repositories/
│   └── manager.py         # Leitura, escrita e operações sobre os dados
├── tests/
│   └── test_api.py        # Testes automatizados com cliente Flask
├── services/
│   └── usuarios.py        # Regras de negócio e sincronização
├── app.py                 # Aplicação Flask e definição das rotas
├── requirements.txt       # Dependências do projeto
├── RELATORIO.md           # Relatório técnico
└── LICENSE                # Licença do projeto
```

## Pré-requisitos

- Python 3.13 ou superior.
- `pip` disponível no ambiente Python.
- Acesso ao terminal.

## Instalação

No Windows, execute os comandos a partir da raiz do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

O ambiente virtual `.venv` é ignorado pelo Git e deve ser ativado sempre que o projeto for executado em uma nova sessão do terminal.

## Execução

Com o ambiente virtual ativado, inicie o servidor com:

```powershell
py app.py
```

Como alternativa, use a CLI do Flask:

```powershell
py -m flask --app app.py run
```

A API estará disponível em `http://127.0.0.1:5000`.

## Endpoints

As rotas do recurso utilizam a barra final (`/`) conforme definido em `app.py`.

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Retorna uma mensagem de boas-vindas. |
| POST | `/usuarios/` | Cadastra um novo usuário. |
| GET | `/usuarios/` | Lista todos os usuários. |
| GET | `/usuarios/<id>/` | Consulta um usuário pelo ID. |
| PUT | `/usuarios/<id>/` | Atualiza os dados de um usuário. |
| DELETE | `/usuarios/<id>/` | Realiza a remoção lógica de um usuário. |

### Criar usuário

```http
POST /usuarios/
Content-Type: application/json

{
	"nome": "Edgar Poema",
	"email": "edgar_poema@exemplo.com"
}
```

Resposta apresentada pela API:

```json
{
	"mensagem": "Usuario adicionado com sucesso!",
	"status_code": 201,
	"success": "Created"
}
```

### Listar e consultar usuários

```http
GET /usuarios/
GET /usuarios/1/
```

Para um ID inexistente, a API retorna um objeto JSON com `status_code` igual a `404` e a mensagem `Usuario nao encontrado.`.

### Atualizar usuário

```http
PUT /usuarios/1/
Content-Type: application/json

{
	"nome": "Edgar Poema Atualizado",
	"email": "edgar.atualizado@exemplo.com"
}
```

### Remover usuário

```http
DELETE /usuarios/1/
```

No estado atual, a remoção é lógica: `nome` e `email` recebem `null`, `estado` passa a `inativo` e o registro não é excluído fisicamente. O `id` é preservado e registros inativos não aceitam `PUT`.

## Validações e respostas

As operações `POST` e `PUT` exigem `Content-Type: application/json` e validam a presença e o preenchimento de `nome` e `email`, o nome formado apenas por letras e espaços, o caractere `@` no e-mail e a unicidade do endereço.

As respostas de erro seguem este formato:

```json
{
	"status_code": 400,
	"error": "Unacceptable",
	"mensagem": "Campos obrigatórios ausentes."
}
```

Os códigos informados no corpo JSON são `400` para dados inválidos, `406` para conteúdo não aceito, `409` para e-mail duplicado e `404` para usuário inexistente.

## Persistência

Os dados são carregados e gravados em `models/dados.json`, inicialmente com a estrutura:

```json
{
	"usuarios": []
}
```

Essa abordagem atende a testes locais e ao objetivo didático do MVP, mas não oferece os recursos de concorrência, transações, controle de acesso e integridade esperados em um banco de dados de produção.

## Testes

Execute a suíte automatizada na raiz do projeto:

```powershell
py -m pytest -q
```

Os testes cobrem criação, consulta, exclusão lógica, bloqueio de alterações, e-mails duplicados, payload inválido e criação concorrente. Para o smoke test contra um servidor em execução, use `py tests\test.py`.

## Concorrência e limitações

- As mutações passam por `services/usuarios.py`, que usa `RLock` para serializar requisições no processo e gravação atômica por arquivo temporário.
- O lock não coordena múltiplos processos ou instâncias do servidor; a migração para banco transacional continua necessária em produção.
- O JSON é carregado em memória e permanece adequado apenas ao MVP local.

## Organização

A organização atual é adequada para o tamanho do projeto. Se crescer, `controllers/` pode ser renomeado para `routes/` ou `api/`, e `validacao.py` para `validators.py`. A separação entre `services/` e `repositories/` já está no local apropriado.

## Próximas melhorias

- Migrar a persistência para um banco de dados transacional.
- Adicionar tratamento centralizado de erros e configuração por variáveis de ambiente.

## Licença

Este projeto está distribuído sob a licença MIT. Consulte [LICENSE](LICENSE) para obter o texto completo.