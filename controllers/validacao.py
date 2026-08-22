# extrai conteúdo do corpo de requisição
def validar_conteudo_json(content):
    """
    Verificar se o corpo de requisição é JSON.

    Args:
        content (str): tipo de conteúdo aceito pelo servidor.

    Returns:
        dict: mensagem de erro, se não for JSON
        None: formato válido
    """

    if content != 'application/json':
        return {"status_code": 406, "error": "Unacceptable", "mensagem":"Recusado. O formato do conteudo deve ser JSON."}
    return None

def validar_campos_e_valores(dados):
    """ 
    Valida os campos e valores do usuário.

    Args:
        dados (dict): os dados do usuário
        
    Returns:
        str: mensagem de erro apenas se os dados forem inválidos.
    """
    # Valida se os campos obrigatórios estão presentes ou existem
    if 'nome' not in dados or 'email' not in dados or not dados['nome'] or not dados['email']:
        return {"status_code": 400, "error": "Unacceptable", "mensagem": "Campos obrigatórios ausentes."}

    # Valida se o email é válido e nome contém apenas letras e espaços
    if not isinstance(dados['nome'], str) or not all(c.isalpha() or c.isspace() for c in dados['nome']):
        return {"status_code": 400, "error": "Unacceptable", "mensagem": "Nome inválido."}

    if not isinstance(dados['email'], str) or '@' not in dados['email']:
        return {"status_code": 400, "error": "Unacceptable", "mensagem": "Email inválido."}

    return None
