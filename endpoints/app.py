
from flask import Flask, request, jsonify
from inserir import insert_funcionario
from consultar import read_funcionario
from atualizar import update_funcionario
from delete import delete_funcionario


from validar import validar_email, validar_cpf, validar_tel, validar_nome, validar_senha


app = Flask(__name__)

 

#criação de novos funcionario
@app.route("/funcionario", methods=['POST'])
def criar_funcionario():
    dados= request.json
    print("API", dados)
    resposta = insert_funcionario(dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400


#rota para listar funcionario
@app.route("/funcionario", methods=['GET'])
def listar_funcionario():
    resposta = read_funcionario()
    return jsonify(resposta)

#atualizar funcionario
@app.route("/funcionario/<int:funcionario_id>", methods=['PUT'])
def atualizar_funcionario(funcionario_id):
    dados = request.json
    dados['funcionario_id'] = funcionario_id
    resposta = update_funcionario(dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400


#rota para excluir funcionario
@app.route('/funcionario/<int:funcionario_id>', methods=['DELETE'])
def excluir_funcionario(funcionario_id):
    resposta = delete_funcionario(funcionario_id)
    return jsonify(resposta)

if __name__ == "__main__":
    app.run(debug=True)

