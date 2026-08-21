# Importa framework Flask e jsonify para criar a API e retornar respostas em formato JSON
from flask import Flask, jsonify, request

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

# extrai conteúdo do corpo de requisição
def extrair_conteudo_json():
    """Extrai o conteudo JSON de uma requisicao ou retornando mensagem de erro"""

    if request.content_type != 'application/json':
        return jsonify({'status_code': 406, 'error': 'Unacceptable', 'mensagem': 'Recusado. O formato do conteudo deve ser JSON.'})
    return None

# Define uma rota para a raiz da API que retorna uma mensagem de boas-vindas em formato JSON
@app.route('/')
def home():
    erro = extrair_conteudo_json()
    if erro:
        return erro
    return jsonify({"mensagem": "Bem-vindo à API Connect!"})

# Define uma rota para a API que retorna informações sobre o status da aplicação
if __name__ == '__main__':
    app.run(debug=True)