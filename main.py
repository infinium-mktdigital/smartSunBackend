from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import database, emails, codes, address, solar

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
        token = codes.generateToken(email)
        return jsonify({"token":token}), 200
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
@token_required
def getUsers(payload):
    try:
        response = database.getAllUsers()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# get lat and long with a zipcode
@app.route('/address/<cep>', methods=['GET'])
@token_required
def getAddress(payload,cep):

    email = payload.get('email')
    request = database.getAddress(email)
    if request:
        return jsonify(request), 200
    try:
        response = address.searchCep(cep)
        database.saveAddress(email,response)
        data = {
            "lat": response['latitude'],
            "lon": response['longitude']
        }
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# get solar data from lat and long
@app.route('/solar', methods=['GET'])
@token_required
def getSolar(payload):
    email = payload.get('email')
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    solarData = database.getSolar(lat, lon)
    response = solarData[0]['solar']
    if response != None:
        return jsonify(response), 200
    try:
        response = solar.request(lat, lon)
        database.saveSolar(email, response)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)