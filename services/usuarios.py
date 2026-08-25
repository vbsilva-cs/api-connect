"""Regras de negócio e sincronização das alterações de usuários."""

from threading import RLock

import repositories.manager as manager


_LOCK = RLock()


def criar_usuario(usuario):
    """Cria um usuário dentro de uma seção crítica."""
    with _LOCK:
        if manager.validar_email(usuario["email"]):
            return None
        usuario_id = manager.gerar_registro()
        return manager.atualizar_registro(usuario_id, usuario)


def atualizar_usuario(usuario_id, usuario):
    """Atualiza usuário ativo, recusando registros inutilizados."""
    with _LOCK:
        registro = manager.obter_usuario_por_("id", usuario_id)
        if registro is None or registro.get("estado") != "ativo":
            return None
        if manager.validar_email(usuario["email"], ignorar_id=usuario_id):
            return None
        return manager.atualizar_registro(usuario_id, usuario)


def inativar_usuario(usuario_id):
    """Inativa logicamente um usuário, preservando seu ID."""
    with _LOCK:
        registro = manager.obter_usuario_por_("id", usuario_id)
        if registro is None:
            return None
        if registro.get("estado") == "inativo":
            return registro.copy()
        dados_inativados = {
            campo: None
            for campo in registro
            if campo not in ("id", "estado")
        }
        dados_inativados["estado"] = "inativo"
        return manager.atualizar_registro(usuario_id, dados_inativados)