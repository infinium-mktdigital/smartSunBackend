import requests, os
from enum import Enum
from dotenv import load_dotenv

class emailTemplate(Enum):
     FIRST_EMAIL = "htmls/firstEmail.html"
     FORGET_PASSWORD = "htmls/forgetPassword.html"
     PASSWORD_CHANGED = "htmls/passwordChanged.html"

def variables():
    load_dotenv(dotenv_path='env/.env')
    apikey = os.getenv("BREVO_API_KEY")
    var = {
        "url":"https://api.brevo.com/v3/smtp/email",
        "header": {
            "accept":"application/json",
            "api-key":apikey,
            "content-type":"application/json"
        }, 
        "sender":{
            "name":"Contato Smart Sun",
            "email":"infinium.mktdigital@gmail.com"
        }
    }
    return var
     

def sendEmail(email, name, emailType: emailTemplate, code=None):
    try:
        var = variables()
        if emailType == emailTemplate.FIRST_EMAIL:
            subject = "Seja bem-vindo(a) - Smart Sun"
        elif emailType == emailTemplate.FORGET_PASSWORD:
            subject = "Redefinição de Senha - Smart Sun"
        else:
            subject = "Senha Alterada - Smart Sun"

        if not name:
            name = "Usuário"

        to = [{"name": name, "email": email}]

        with open(emailType.value, "r", encoding="utf-8") as file:
            html_content = file.read()

        if emailType == emailTemplate.FORGET_PASSWORD:
            html_content = html_content.replace("{{code}}", str(code))

        data = {
            "sender": var["sender"],
            "to": to,
            "subject": subject,
            "htmlContent": html_content,
        }

        response = requests.post(var["url"], headers=var["header"], json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
