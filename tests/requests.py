import requests

url = 'http://127.0.0.1:5000/usuarios/'

# Testes com requisições

# Criação com sucesso (201)
r = requests.post(url, json={"nome": "Edgar Poema", "email": "edgar_poema@exemplo.com"})
print(r.json(), "\n")

# Criação com falha que não contém o campo "email" (400)
r = requests.post(url, json={"nome": "Roberto Carlos"})
print(r.json(), "\n")

# Listagem de todos os usuários (200)

r = requests.get(url)
print(r.json(), "\n")

# Procura de um usuário através de um ID inexistente (404)
r = requests.get(f"{url}/999")
print(r.json(), "\n")