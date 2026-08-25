"""Acesso à persistência JSON dos usuários."""

import json
import os
from pathlib import Path


CAMINHO = Path(__file__).resolve().parent.parent / "models" / "dados.json"
# Mantém compatibilidade com código externo que ainda usa o nome antigo.
caminho = CAMINHO


def _normalizar_dados(dados):
    """Garante o estado padrão nos registros legados."""
    for usuario in dados.get("usuarios", []):
        usuario.setdefault("estado", "ativo")
    return dados

def carregar_dados():
    """Carrega e normaliza os dados persistidos."""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return _normalizar_dados(json.load(arquivo))


def _salvar_dados():
    """Grava o conteúdo em arquivo temporário e o substitui atomicamente."""
    caminho_temporario = Path(f"{caminho}.tmp")
    with open(caminho_temporario, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        arquivo.flush()
        os.fsync(arquivo.fileno())
    os.replace(caminho_temporario, caminho)


def gerar_registro():
    """Cria um registro reservado e retorna seu ID monotônico."""
    global dados
    novo_id = max((usuario["id"] for usuario in dados["usuarios"]), default=0) + 1
    dados["usuarios"].append({"id": novo_id, "estado": "ativo"})
    _salvar_dados()
    return novo_id


def atualizar_registro(id, usuario):
    """Atualiza um registro e retorna sua cópia, ou ``None`` se ausente."""
    global dados
    pessoa = obter_usuario_por_("id", id)
    if pessoa is None:
        return None
    pessoa.update(usuario)
    _salvar_dados()
    return pessoa.copy()


def obter_usuario_por_(atributo, valor):
    """Retorna o primeiro usuário que corresponde ao atributo informado."""
    for pessoa in dados["usuarios"]:
        if pessoa[atributo] == valor:
            return pessoa
    return None


def validar_email(endereco, ignorar_id=None):
    """Retorna erro quando um registro ativo já usa o endereço informado."""
    for pessoa in dados["usuarios"]:
        if (
            pessoa.get("estado") == "ativo"
            and pessoa.get("email") == endereco
            and pessoa["id"] != ignorar_id
        ):
            return {"status_code": 409, "error": "Unacceptable", "mensagem": "Email já cadastrado."}
    return None

dados = carregar_dados()
