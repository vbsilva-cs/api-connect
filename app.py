# Importa Flask e jsonify para criar a API e retornar respostas JSON.
from flask import Flask, jsonify, request
from controllers.validacao import validar_conteudo_json, validar_campos_e_valores
import repositories.manager as mng
from services import usuarios as servico_usuarios

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"mensagem": "Bem-vindo à API Connect!"})


@app.route("/usuarios/", methods=["POST"])
def adicionar_usuario():
    # valida conteudo JSON
    erro = validar_conteudo_json(request.content_type)
    if erro:
        return jsonify(erro), 406

    # coleta e valida dados de corpo de requisição
    dados_usuario = request.get_json()
    erro = validar_campos_e_valores(dados_usuario)
    if erro:
        return jsonify(erro), 400

    usuario = servico_usuarios.criar_usuario(dados_usuario)
    if usuario is None:
        return jsonify({
            "status_code": 409,
            "error": "Unacceptable",
            "mensagem": "Email já cadastrado.",
        }), 409
    return jsonify({
        "status_code": 201,
        "success": "Created",
        "mensagem": "Usuario adicionado com sucesso!",
    }), 201

@app.route("/usuarios/", methods=["GET"])
def exibir_todos_os_usuarios():
    dados_usuarios = mng.carregar_dados()
    return jsonify({
        "status_code": 200, 
        "success": "OK", 
        "mensagem": dados_usuarios,
    }), 200


@app.route("/usuarios/<int:user_id>/", methods=["GET"])
def exibir_usuario_por_id(user_id):
    usuario = mng.obter_usuario_por_("id", user_id)
    if usuario:
        return jsonify({
            "status_code": 200, 
            "success": "OK", 
            "mensagem": usuario,
        }), 200    
    else:
        return jsonify({
            "status_code": 404,
            "error": "Not Found",
            "mensagem": "Usuario nao encontrado.",
        }), 404

@app.route("/usuarios/<int:user_id>/", methods=["PUT"])
def atualizar_usuario(user_id):
    erro = validar_conteudo_json(request.content_type)
    if erro:
        return jsonify(erro), 406
    
    # coleta dados de corpo de requisição
    dados_usuario = request.get_json()

    erro = validar_campos_e_valores(dados_usuario)
    if erro:
        return jsonify(erro), 400
    
    # verifica ID na base de dados
    usuario = mng.obter_usuario_por_("id", user_id)
    if not usuario:
        return jsonify({
            "status_code": 404,
            "error": "Not Found",
            "mensagem": "Usuario nao encontrado.",
        }), 404
    
    # Atualiza o usuário na base de dados
    usuario_atualizado = servico_usuarios.atualizar_usuario(user_id, dados_usuario)
    if usuario_atualizado:
        return jsonify({"status_code": 200, "success": "OK", "mensagem": usuario_atualizado}), 200
    if usuario.get("estado") == "inativo":
        return jsonify({
            "status_code": 409,
            "error": "Conflict",
            "mensagem": "Registro inativo não pode ser alterado.",
        }), 409
    if mng.validar_email(dados_usuario["email"], ignorar_id=user_id):
        return jsonify({
            "status_code": 409,
            "error": "Unacceptable",
            "mensagem": "Email já cadastrado.",
        }), 409
    else:
        #
        return jsonify({
            "status_code": 500, 
            "error": "", 
            "mensagem": "Erro ao atualizar o usuário.",
        }), 500

            

@app.route("/usuarios/<int:user_id>/", methods=["DELETE"])
def deletar_usuario(user_id):
    # verifica ID na base de dados
    usuario = mng.obter_usuario_por_("id", user_id)
    if not usuario:
        return jsonify({
            "status_code": 404, 
            "error": "Not Found", 
            "mensagem": "Usuario nao encontrado.",
        }),404

    dados_removidos = servico_usuarios.inativar_usuario(user_id)
    return jsonify({
        "status_code": 200, 
        "success": "OK", 
        "mensagem": dados_removidos,
    }), 200
    
# Define uma rota para a API que retorna informações sobre o status da aplicação
if __name__ == "__main__":
    app.run()