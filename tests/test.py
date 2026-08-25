import requests

url = 'http://127.0.0.1:5000/usuarios/'


# Deleção com sucesso (200)
r = requests.delete(f'{url}/2')
assert r.status_code == 200


# Criação com sucesso (201) ou erro por email duplicado (409)
r = requests.post(url, json={"nome": "John Doe", "email": "john_doe@exemplo.com"})
assert r.status_code == 201 or 409


# Criação com falha que não contém o campo "email" (400)
r = requests.post(url, json={"nome": "Roberto Carlos"})
assert r.status_code == 400


# Listagem de todos os usuários (200)
r = requests.get(url)
assert r.status_code == 200


# Procura de um usuário através de um ID inexistente (404)
r = requests.get(f"{url}/999")
assert r.status_code == 404


print("Teste finalizado com sucesso.")