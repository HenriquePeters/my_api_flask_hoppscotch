from flask import Flask, jsonify, request
from flask_cors import CORS

# Cria a instância da aplicação Flask
app = Flask(__name__)
CORS(app)

# Dados iniciais de produtos (simulando um banco de dados)
produtos = [
    {'id': 1, 'nome': 'Camiseta', 'preco': 49.90, 'estoque': 10},
    {'id': 2, 'nome': 'Calça Jeans', 'preco': 129.90, 'estoque': 5},
    {'id': 3, 'nome': 'Tênis Esportivo', 'preco': 299.99, 'estoque': 8}
]

# ---------------- ROTAS ----------------

# GET /produtos - listar todos os produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    return jsonify(produtos)

# GET /produtos/<id> - obter um produto específico
@app.route('/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    return jsonify(produto)

# POST /produtos - criar um novo produto
@app.route('/produtos', methods=['POST'])
def criar_produto():
    if not request.json or not all(k in request.json for k in ['nome', 'preco', 'estoque']):
        return jsonify({'erro': 'Requisição deve conter nome, preco e estoque'}), 400

    novo_produto = {
        'id': produtos[-1]['id'] + 1 if produtos else 1,
        'nome': request.json['nome'],
        'preco': request.json['preco'],
        'estoque': request.json['estoque']
    }
    produtos.append(novo_produto)
    return jsonify(novo_produto), 201

# PUT /produtos/<id> - atualizar um produto
@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    produto['nome'] = request.json.get('nome', produto['nome'])
    produto['preco'] = request.json.get('preco', produto['preco'])
    produto['estoque'] = request.json.get('estoque', produto['estoque'])
    return jsonify(produto)

# DELETE /produtos/<id> - deletar um produto
@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    produtos.remove(produto)
    return jsonify({'resultado': 'Produto deletado com sucesso'})

# DESAFIO EXTRA - POST /produtos/<id>/comprar
@app.route('/produtos/<int:produto_id>/comprar', methods=['POST'])
def comprar_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    if produto['estoque'] <= 0:
        return jsonify({'erro': 'Produto fora de estoque'}), 400

    produto['estoque'] -= 1
    return jsonify(produto)

# Executa a aplicação
if __name__ == '__main__':
    app.run(debug=True)
