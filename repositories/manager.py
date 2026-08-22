import json

# Define o caminho para o arquivo JSON que contém a base de usuários
caminho = 'models/dados.json'

def carregar_dados():
    """ 
    Carrega informações da base de dados.
     
    Returns:
        dict
    """
    with open(caminho, 'r') as file:
        dados_dict = json.load(file)
    return dados_dict


def gerar_registro():
    """
    Gera registro com ID único para um novo objeto no banco de dados.

    Returns:
        int: código do novo ID.
    """
    global dados
    if not dados['usuarios'][0]['id']:
        dados['usuarios'] = []
        novo_id = 1
    else:
        novo_id = dados['usuarios'][-1]['id'] + 1

    dados['usuarios'].append({'id': novo_id})

    with open(caminho, 'w') as file:
        json.dump(dados, file, indent=4)

    return novo_id


def atualizar_registro(id, usuario):
    """ 
    Atualiza os campos de um registro com ID especificado.

    Args:
        id(int): código identificador único do registro.
        usuario (dict): dados para inserção.
    """
    global dados
    for pessoa in dados['usuarios']:
        if pessoa['id'] == id:
            for campo, valor in usuario.items():
                pessoa[campo] = valor
        
    with open(caminho, 'w') as file:
        json.dump(dados, file, indent=4)
        
    return None


def obter_usuario_por_(atributo, valor):
    for pessoa in dados['usuarios']:
        if pessoa[atributo] == valor:
            return pessoa
    return None


def validar_email(endereco):
    """
    Valida se o email já existe na base de dados.

    Args:
        entrada (str): endereço eletrônico para comparação

    Returns:
        str: mensagem de erro apenas se houver duplicatas
    """
    for pessoa in dados['usuarios']:
        if pessoa['email'] == endereco:
            return {"status_code": 409, "error": "Unacceptable", "mensagem": "Email já cadastrado."}
    return None

dados = carregar_dados()