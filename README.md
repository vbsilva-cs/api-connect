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
- `requests` para os testes manuais
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
│   └── test.py        # Testes manuais com requisições HTTP
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
py -m pip install requests
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

No estado atual, a remoção é lógica: os campos diferentes de `id` recebem `null` no arquivo JSON. O registro não é excluído fisicamente da coleção.

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

## Testes manuais

Com o servidor em execução, abra outro terminal, ative o ambiente virtual e execute:

```powershell
py tests\test.py
```

O script testa a criação de usuário, a validação de um cadastro sem e-mail, a listagem e a consulta de um ID inexistente. Os resultados esperados no corpo JSON são, respectivamente, `201`, `400`, `200` e `404`.

O arquivo atual imprime as respostas, mas não possui asserções automatizadas; trata-se, portanto, de um teste manual de integração.

## Limitações conhecidas

- A função de geração de IDs precisa tratar explicitamente a coleção vazia antes de acessar o primeiro elemento.
- A persistência depende do diretório a partir do qual o processo é iniciado, pois o caminho do arquivo JSON é relativo.
- O estado global e a escrita direta em arquivo são inadequados para múltiplas requisições concorrentes.

## Licença

Este projeto está distribuído sob a licença MIT. Consulte [LICENSE](LICENSE) para obter o texto completo.
