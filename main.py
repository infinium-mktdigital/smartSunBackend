from flask import Flask, request, jsonify
from collections import OrderedDict
from flask_cors import CORS
from functools import wraps
import database, emails, codes, address, solar, calc
import ast

app = Flask(__name__)
CORS(app)

# define a token to authorize authenticated users use the platform
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token é obrigatório!'}), 401

        payload = codes.verifyToken(token)
        if not payload:
            return jsonify({'message': 'Token inválido ou expirado!'}), 401
        return f(payload, *args, **kwargs)
    return decorated

# create user on supabase and send a welcome email
@app.route('/user',methods=['POST'])
def create():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    try:
        response = database.createUser(name,email,password)
        data = ast.literal_eval(response)
        if data['code'] == '23505':
            return jsonify({"message": "Email já cadastrado"}), 406
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    emails.sendEmail(email,name,emails.emailTemplate.FIRST_EMAIL)
    return jsonify(response), 200

# verify if the login credentials are valids
@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    
    try:
        response = database.searchUser(email,password)
        if response == True:
            token = codes.generateToken(email)
        else:
            return jsonify({"message": "Credenciais inválidas"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"token":token}), 200

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
@token_required
def getUsers(payload):
    try:
        response = database.getAllUsers()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# get a specific user by email
@app.route('/user/<email>', methods=['GET'])
def getUser(email):
    try:
        response = database.getUser(email)
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# make a calc for the seller
@app.route('/solar/calculate', methods=['POST'])
@token_required
def calculateSolar(payload):    
    try:
        data = request.get_json()
        cep = data.get('cep')
        consumo = data.get('consumo')
        cost = data.get('cost')
                    
        email = payload.get('email')
        
        address_response = address.searchCep(cep)
        database.saveAddress(email, address_response)
        lat = address_response['latitude']
        lon = address_response['longitude']
    
        solar_data = database.getSolar(lat, lon)
        if solar_data and solar_data[0]['solar']:
            solar_response = solar_data[0]['solar']
        else:
            solar_response = solar.request(lat, lon)
            database.saveSolar(lat, lon, solar_response)
        
        if isinstance(solar_response, (int, float)):
            solar_irradiance = float(solar_response)
        elif isinstance(solar_response, dict):
            solar_irradiance = solar_response.get('irradiance') or solar_response.get('ghi') or solar_response.get('solar_irradiance')
        else:
            return jsonify({"error": "Formato de dados solares inválido"}), 500
        
        if not solar_irradiance:
            return jsonify({"error": "Dados de irradiância solar não encontrados"}), 500
            
        panel_calculation = calc.calcular_sistema_solar(consumo,solar_irradiance,cost)
        database.saveCalc(email, panel_calculation)
        
        return jsonify(panel_calculation), 200
        
    except ValueError as e:
        return jsonify({"error": f"Erro de validação: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

# return all the calcs from an email
@app.route('/solar/calculate/<email>', methods=['GET'])
def getCalc(email):
    try:
        response = database.getCalc(email)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# return details of a specific calc
@app.route('/solar/calculate/<identifier>', methods=['GET'])
def getCalcById(identifier):
    try:
        response = database.getCalcDetails(int(identifier))
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)