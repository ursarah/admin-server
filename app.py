from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json

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
        json.dump(dados, file)


ALUNOS = carregar_dados()


@app.route('/', methods=['POST', 'GET'])
def metodos_http():
    if request.method == 'GET':
        return jsonify(ALUNOS)

    if request.method == 'POST':
        user = request.get_json()

        if user['nome'] == '' or user['email'] == '' or user['telefone'] == '' or user['bairro'] == '':
            return Response(status=400)
        else:
            dict_aluno = {
                "id": 1,
                "nome": user['nome'],
                "telefone": user['telefone'],
                "email": user['email'],
                "bairro": user['bairro'],
            }
            for aluno in ALUNOS:
                if aluno['id'] == dict_aluno['id']:
                    dict_aluno['id'] += 1

            ALUNOS.append(dict_aluno)
            salvar_dados(ALUNOS)
            return Response(status=200)

    if request.method == 'DELETE':
        ...


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    global ALUNOS
    ALUNOS = [aluno for aluno in ALUNOS if aluno['id'] != id]
    salvar_dados(ALUNOS)
    return Response(200)


if __name__ == "__main__":
    app.run(debug=True)
