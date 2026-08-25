import requests

url = 'http://127.0.0.1:5000/usuarios/'

try:
    # Deleção com sucesso (200)
    r = requests.delete(f'{url}2')
    assert r.status_code == 200


    # Criação com sucesso (201) ou erro por email duplicado (409)
    r = requests.post(url, json={"nome": "Usuário Teste", "email": "usuario_teste@exemplo.com"})
    assert r.status_code in (201, 409)


    # Criação com falha que não contém o campo "email" (400)
    r = requests.post(url, json={"nome": "Roberto Carlos"})
    assert r.status_code == 400


    # Listagem de todos os usuários (200)
    r = requests.get(url)
    assert r.status_code == 200


    # Procura de um usuário através de um ID inexistente (404)
    r = requests.get(f"{url}999/")
    assert r.status_code == 404


    print("Teste finalizado sem erros.")

except AssertionError:
    print("Atenção! Inconsistências foram identificadas!")