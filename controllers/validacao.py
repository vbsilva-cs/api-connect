"""Validações dos dados recebidos pela API."""


def validar_conteudo_json(content):
    """Verifica se o corpo da requisição usa JSON."""

    if content != 'application/json':
        return {
            "status_code": 406,
            "error": "Unacceptable",
            "mensagem": "Recusado. O formato do conteudo deve ser JSON.",
        }
    return None

def validar_campos_e_valores(dados):
    """Valida campos obrigatórios e tipos do usuário."""
    if not isinstance(dados, dict):
        return {"status_code": 400, "error": "Unacceptable", "mensagem": "JSON inválido."}

    # Valida se os campos obrigatórios estão presentes ou existem
    if "nome" not in dados or "email" not in dados or not dados["nome"] or not dados["email"]:
        return {
            "status_code": 400,
            "error": "Unacceptable",
            "mensagem": "Campos obrigatórios ausentes.",
        }

    # Valida se o email é válido e nome contém apenas letras e espaços
    if not isinstance(dados["nome"], str) or not all(c.isalpha() or c.isspace() for c in dados["nome"]):
        return {"status_code": 400, "error": "Unacceptable", "mensagem": "Nome inválido."}

    if not isinstance(dados["email"], str) or "@" not in dados["email"]:
        return {"status_code": 400, "error": "Unacceptable", "mensagem": "Email inválido."}

    return None
