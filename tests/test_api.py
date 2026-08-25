"""Testes automatizados do fluxo HTTP de usuários."""

import json
from concurrent.futures import ThreadPoolExecutor

import pytest

import repositories.manager as manager
from app import app
from services import usuarios as service


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """Fornece cliente Flask com persistência temporária."""
    caminho_original = manager.caminho
    dados_originais = manager.dados
    caminho_teste = tmp_path / "dados.json"
    caminho_teste.write_text(json.dumps({"usuarios": []}), encoding="utf-8")
    monkeypatch.setattr(manager, "caminho", caminho_teste)
    monkeypatch.setattr(manager, "dados", manager.carregar_dados())
    with app.test_client() as cliente:
        yield cliente
    manager.caminho = caminho_original
    manager.dados = dados_originais


def criar(client, nome="Ana Silva", email="ana@example.com"):
    """Cria usuário para os cenários do teste."""
    return client.post("/usuarios/", json={"nome": nome, "email": email})


def test_criacao_consulta_e_id_monotono_apos_delete(client):
    """DELETE preserva o registro e o próximo ID."""
    assert criar(client).status_code == 201
    assert client.delete("/usuarios/1/").status_code == 200
    registro = client.get("/usuarios/1/").get_json()["mensagem"]
    assert registro == {"id": 1, "nome": None, "email": None, "estado": "inativo"}
    assert criar(client, "Bruno Lima", "bruno@example.com").status_code == 201
    assert client.get("/usuarios/2/").get_json()["mensagem"]["id"] == 2


def test_registro_inativo_nao_pode_ser_alterado(client):
    """PUT retorna conflito e preserva os dados inutilizados."""
    criar(client)
    client.delete("/usuarios/1/")
    resposta = client.put("/usuarios/1/", json={"nome": "Novo Nome", "email": "novo@example.com"})
    assert resposta.status_code == 409
    assert client.get("/usuarios/1/").get_json()["mensagem"]["estado"] == "inativo"


def test_email_duplicado_e_json_invalido(client):
    """Valida conflitos de e-mail e payloads que não são objetos."""
    assert criar(client).status_code == 201
    assert criar(client, "Outra Pessoa", "ana@example.com").status_code == 409
    resposta = client.post(
        "/usuarios/",
        data="null",
        content_type="application/json",
    )
    assert resposta.status_code == 400


def test_criacoes_concorrentes_geram_ids_distintos(client):
    """O lock do serviço serializa reservas de ID."""
    with ThreadPoolExecutor(max_workers=5) as executor:
        registros = list(executor.map(
            lambda indice: service.criar_usuario({
                "nome": f"Pessoa {indice}",
                "email": f"p{indice}@example.com",
            }),
            range(5),
        ))
    assert all(registro["estado"] == "ativo" for registro in registros)
    ids = [usuario["id"] for usuario in manager.dados["usuarios"]]
    assert ids == [1, 2, 3, 4, 5]