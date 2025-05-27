import hashlib, secrets, jwt, datetime, os
from dotenv import load_dotenv
load_dotenv()

def sha256(password):
    string = password
    encoded_string = string.encode('utf-8')
    hash_object = hashlib.sha256(encoded_string)
    hex_digest = hash_object.hexdigest()
    return hex_digest

def forgetPass():
    code = secrets.randbelow(900000)+100000
    return code

def generateToken(email):
    payload = {
        'email': email,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=48)
    }
    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
    return token

def verifyToken(token):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None