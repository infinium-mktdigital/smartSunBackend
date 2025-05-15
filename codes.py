import hashlib, secrets

def sha256(password):
    string = password
    encoded_string = string.encode('utf-8')
    hash_object = hashlib.sha256(encoded_string)
    hex_digest = hash_object.hexdigest()
    return hex_digest

def forgetPass():
    code = secrets.randbelow(900000)+100000
    return code