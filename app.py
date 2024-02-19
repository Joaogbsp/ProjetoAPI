from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.db'

db = SQLAlchemy(app)

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    editora = db.Column(db.String(100), nullable=False)
    ano_edicao = db.Column(db.String(4), nullable=False)
    genero = db.Column(db.String(100), nullable=False)
    emprestou = db.Column(db.Boolean, nullable=False)
    prazo_devolucao = db.Column(db.String(10), nullable=True)

@app.route('/livros/<int:livro_id>', methods=['GET'])
def obter_livro_por_id(livro_id):
    livro = Livro.query.get(livro_id)

    if not livro:
        return jsonify({'mensagem': 'Livro não encontrado'}), 404

    livro_dados = OrderedDict({
        'id': livro.id,
        'titulo': livro.titulo,
        'autor': livro.autor,
        'editora': livro.editora,
        'ano_edicao': livro.ano_edicao,
        'genero': livro.genero,
        'emprestou': livro.emprestou,
        'prazo_devolucao': livro.prazo_devolucao
    })

    return jsonify(livro_dados)

@app.route('/livros', methods=['POST'])
def cadastrar_livro():
    data = request.get_json()
    novo_livro = Livro(**data)
    db.session.add(novo_livro)
    db.session.commit()
    return jsonify({'mensagem': 'Livro cadastrado com sucesso!'}), 201

@app.route('/livros', methods=['GET'])

def buscar_livros():
    livros = Livro.query.all()
    resultado = []
    for livro in livros:
        resultado.append({
            'titulo': livro.titulo,
            'autor': livro.autor,
            'editora': livro.editora,
            'ano_edicao': livro.ano_edicao,
            'genero': livro.genero,
            'emprestou': 'sim' if livro.emprestou else 'nao',
            'prazo_devolucao': livro.prazo_devolucao
        })
    return jsonify(resultado)

@app.route('/livros/<int:livro_id>', methods=['PUT'])

def atualizar_livro(livro_id):
    livro = Livro.query.get(livro_id)
    if not livro:
        return jsonify({'mensagem': 'Livro não encontrado'}), 404
    dados_atualizados = request.get_json()
    for campo, valor in dados_atualizados.items():
        setattr(livro, campo, valor)
    db.session.commit()

    return jsonify({'mensagem': 'Livro atualizado com sucesso'})

@app.route('/livros/<int:livro_id>', methods=['DELETE'])

def excluir_livro(livro_id):
    livro = Livro.query.get(livro_id)

    if not livro:
        return jsonify({'mensagem': 'Livro não encontrado'}), 404

    db.session.delete(livro)
    db.session.commit()

    return jsonify({'mensagem': 'Livro excluído com sucesso'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
