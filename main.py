from flask import Flask, request, jsonify
from flask_cors import CORS
import database, emails, os

app = Flask(__name__)
CORS(app)

# create user on supabase and send a welcome email
@app.route('/user',methods=['POST'])
def create():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    response = database.createUser(name,email,password)
    emails.sendEmail(email,name,emails.emailTemplate.FIRST_EMAIL)

    return jsonify(response.data)

# verify if the login credentials are valids
@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    response = database.searchUser(email,password)
    if response == True:
        return jsonify({"message": "Login bem-sucedido"}), 200
    else:
        return jsonify({"message": "Credenciais inválidas"}), 404
    
# create a expiration token for pass
@app.route('/pass/<email>', methods=['GET'])
def forgetPass(email):
    try:
        response = database.resetPass(email)
        if isinstance(response, int) and len(str(response)) == 6:
            emails.sendEmail(email, "", emails.emailTemplate.FORGET_PASSWORD, response)
            return jsonify({"code": response}), 200
        else:
            return jsonify({"error": response}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# validate if the token for pass is correctly
@app.route('/pass',methods=["POST"])
def verifyToken():
    data = request.get_json()

    email = data.get("email")
    code = data.get("code")

    response = database.verifyPass(email,code)
    if response == True:
        return jsonify({"message": "O token está correto"}), 200
    else:
        return jsonify({"message": "Token incorreto"}), 404

# update a password
@app.route('/pass/new',methods=["POST"])
def updatePass():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    response = database.updatePass(email,password)
    if bool(response.data):
        emails.sendEmail(email,"",emails.emailTemplate.PASSWORD_CHANGED)
        return jsonify({"message": "Senha atualizada"}),200
    else:
        return jsonify({"message": f"erro ao atualizar a senha"}),404

# get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        response = database.getAllUsers()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)