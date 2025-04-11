from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)


def carregar_dados():
    try:
        with open('database/alunos.json', 'r') as file:
            return json.load(file)
    except:
        return []


def salvar_dados(dados):
    with open('database/alunos.json', 'w') as file:
        json.dump(dados, file, sort_keys=True)


ALUNOS = carregar_dados()


@app.route('/', methods=['POST', 'GET'])
def metodos_http():
    if request.method == 'GET':
        return jsonify(ALUNOS)

    if request.method == 'POST':
        user = request.get_json()

        if user['nome'] == '' or user['email'] == '' or user['telefone'] == '' or user['bairro'] == '':
            return '', 400
        else:
            id = random.randint(0, 999999)
            dict_aluno = {
                "contagem_aluno": 1,
                "id": id,
                "nome": user['nome'],
                "telefone": user['telefone'],
                "email": user['email'],
                "bairro": user['bairro'],
            }
            for aluno in ALUNOS:
                if aluno['contagem_aluno'] == dict_aluno['contagem_aluno']:
                    dict_aluno['contagem_aluno'] = len(ALUNOS) + 1

            ALUNOS.append(dict_aluno)
            salvar_dados(ALUNOS)
            return '', 200


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    global ALUNOS
    ALUNOS = [aluno for aluno in ALUNOS if aluno['id'] != id]
    salvar_dados(ALUNOS)
    return '', (200)


@app.route('/edit/<int:id>', methods=['PATCH'])
def edit_aluno(id):
    global ALUNOS
    userBody = request.get_json()

    if userBody['nome'] == '' and userBody['email'] == '' and userBody['telefone'] == '' and userBody['bairro'] == '':
        return '', 400
    else:
        fields = ['nome', 'email', 'telefone', 'bairro']

        for aluno in ALUNOS:
            if aluno['id'] == id:
                for field in fields:
                    if userBody[field] != '':
                        aluno[field] = userBody[field]
        salvar_dados(ALUNOS)
        return '', 200


if __name__ == "__main__":
    app.run(debug=True)
