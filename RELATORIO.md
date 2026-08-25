# API Connect

## Relatório técnico

### 1. Visão geral

API Connect é uma API REST desenvolvida em Python com Flask para o gerenciamento de usuários. O projeto foi construído como um MVP acadêmico, com persistência local em arquivo JSON e foco na aplicação dos fundamentos de HTTP, arquitetura cliente-servidor, validação de entradas e organização modular do código.

O sistema disponibiliza operações para criação, consulta, atualização e remoção lógica de usuários. As respostas são serializadas em JSON e incluem informações sobre o resultado da operação.

### 2. Objetivos

- Implementar um servidor HTTP funcional com Flask.
- Disponibilizar endpoints REST para o recurso `usuarios`.
- Aplicar os métodos HTTP GET, POST, PUT e DELETE.
- Validar o tipo de conteúdo e os campos recebidos pelo cliente.
- Simular a persistência de dados por meio de um arquivo JSON.
- Separar responsabilidades entre aplicação, validação, acesso a dados e testes.

### 3. Tecnologias e ambiente

- Python 3.13.5.
- Flask 3.1.3.
- `pytest` para os testes automatizados e `requests` para o smoke test HTTP.
- Arquivo JSON como mecanismo de persistência provisória.
- Git para controle de versão.

As dependências da aplicação Flask estão registradas em `requirements.txt`. O ambiente virtual recomendado é `.venv`, mantido fora do controle de versão pelo `.gitignore`.

#### Instalação

No Windows, a preparação do ambiente pode ser realizada com:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

Caso o script de testes seja executado, instale também a biblioteca cliente HTTP:

```powershell
py -m pip install requests
```

### 4. Arquitetura e organização

O projeto adota uma separação simples de responsabilidades, adequada ao escopo do MVP:

```text
/api-connect
    /controllers
        validacao.py
    /models
        dados.json
    /repositories
        manager.py
    /tests
        test_api.py
    /services
        usuarios.py
    app.py
    LICENSE
    README.md
    RELATORIO.md
    requirements.txt
```

- `app.py`: ponto de entrada da aplicação, definição das rotas e coordenação do fluxo HTTP.
- `controllers/validacao.py`: validação do tipo de conteúdo, dos campos obrigatórios, do nome e do e-mail.
- `repositories/manager.py`: leitura e gravação atômica do JSON, geração de identificadores, consulta, atualização e verificação de e-mails duplicados.
- `services/usuarios.py`: regras de negócio das mutações e sincronização por lock de processo.
- `models/dados.json`: armazenamento local dos registros. O estado inicial contém uma coleção `usuarios` vazia.
- `tests/test.py`: script de testes manuais que envia requisições HTTP para a API.
- `requirements.txt`: declaração das dependências Python.
- `README.md`: documentação de uso do projeto.
- `LICENSE`: licença do repositório.

### 5. Inicialização do servidor

O arquivo `app.py` instancia o Flask, importa os módulos de validação e persistência e registra as rotas do recurso `usuarios`. A execução direta inicia o servidor de desenvolvimento na porta padrão 5000:

```powershell
py app.py
```

Também é possível iniciar a aplicação com a CLI do Flask:

```powershell
py -m flask --app app.py run
```

O servidor fica disponível em `http://127.0.0.1:5000`.

### 6. Persistência

A persistência é realizada por `repositories/manager.py`. Na inicialização, a função `carregar_dados()` lê `models/dados.json` e armazena o conteúdo na variável global `dados`. As operações de escrita serializam novamente essa estrutura no mesmo arquivo.

O formato inicial do arquivo é:

```json
{
    "usuarios": []
}
```

Cada usuário possui `id`, `nome`, `email` e `estado`, cujo valor é `ativo` ou `inativo`. O identificador é numérico, monotônico e nunca é reutilizado. O `DELETE` atribui `null` aos dados pessoais e muda o estado para `inativo`; o ID permanece no arquivo. Registros inativos não podem ser alterados.

### 7. Endpoints disponíveis

As rotas utilizam a barra final conforme definidas em `app.py`.

| Método | Endpoint | Finalidade | Resultado previsto |
|---|---|---|---|
| GET | `/` | Verificar a disponibilidade da API | JSON de boas-vindas |
| POST | `/usuarios/` | Criar um usuário | 201 informado na resposta JSON |
| GET | `/usuarios/` | Listar usuários | 200 informado na resposta JSON |
| GET | `/usuarios/<id>/` | Consultar um usuário por ID | 200 ou 404 informado na resposta JSON |
| PUT | `/usuarios/<id>/` | Atualizar um usuário | 200, 404 ou erro de validação informado na resposta JSON |
| DELETE | `/usuarios/<id>/` | Remover logicamente um usuário | 200 ou 404 informado na resposta JSON |

#### Exemplo de criação

```http
POST /usuarios/
Content-Type: application/json

{
    "nome": "Edgar Poema",
    "email": "edgar_poema@exemplo.com"
}
```

Resposta de sucesso:

```json
{
    "mensagem": "Usuario adicionado com sucesso!",
    "status_code": 201,
    "success": "Created"
}
```

#### Exemplo de consulta por ID

```http
GET /usuarios/1/
```

Quando o registro não existe, a API retorna uma mensagem informando a ausência do usuário e o código `404` no corpo JSON.

### 8. Validação e respostas

As operações POST e PUT verificam:

- presença dos campos `nome` e `email`;
- preenchimento dos campos obrigatórios;
- nome composto apenas por letras e espaços;
- presença do caractere `@` no e-mail;
- inexistência de outro usuário com o mesmo e-mail.

Também é validado o `Content-Type` da requisição, que deve ser `application/json`. Os erros são representados por objetos JSON com as chaves `status_code`, `error` e `mensagem`. Entre os códigos previstos estão `400` para dados inválidos, `406` para formato não aceito, `409` para e-mail duplicado e `404` para usuário inexistente.

### 9. Testes realizados

O arquivo `tests/test_api.py` utiliza o cliente Flask para exercitar os seguintes cenários:

1. criação de usuário com dados válidos;
2. tentativa de criação sem o campo `email`;
3. listagem dos usuários cadastrados;
4. consulta de um ID inexistente.

Além desses cenários, a suíte verifica exclusão lógica, preservação do ID, bloqueio de `PUT`, e-mail duplicado, JSON inválido e cinco criações concorrentes.

Para executar os testes automatizados:

```powershell
py -m pytest -q
```

O script `tests/test.py` permanece disponível como smoke test HTTP para ser executado com o servidor em funcionamento.

### 10. Limitações e pontos de evolução

O estado atual atende ao objetivo didático do MVP, mas possui pontos que devem ser tratados antes de uma utilização produtiva:

- as mutações são serializadas por `RLock` em `services/usuarios.py` e a substituição do JSON é atômica;
- o lock funciona dentro de uma instância do processo, não entre múltiplos processos;
- o JSON continua sem transações, histórico ou bloqueio distribuído;
- a validação de e-mail é deliberadamente básica e deve ser fortalecida conforme os requisitos do domínio;
- a persistência em arquivo permanece apropriada apenas ao MVP local.

Como organização, a estrutura atual é adequada ao MVP. Se crescer, `controllers/` pode ser renomeado para `routes/` ou `api/`, `validacao.py` para `validators.py`, e as rotas podem ser movidas de `app.py` para um blueprint. A separação entre serviço e repositório já está no local correto.

### 11. Conclusão

O projeto API Connect implementa uma API REST funcional para gerenciamento de usuários e demonstra os principais conceitos solicitados na experiência prática: inicialização de servidor Flask, definição de rotas, uso de métodos HTTP, validação de dados, respostas JSON, persistência local e organização modular do código.

A solução é adequada como protótipo educacional e fornece uma base clara para futuras melhorias. A análise das limitações registradas é parte importante da avaliação técnica, pois evidencia a diferença entre uma implementação funcional para testes locais e uma API preparada para produção.
