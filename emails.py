import requests
from enum import Enum

class emailTemplate(Enum):
     FIRST_EMAIL = "htmls/firstEmail.html"
     FORGET_PASSWORD = "htmls/forgetPassword.html"
     PASSWORD_CHANGED = "htmls/passwordChanged.html"

def variables():
    apikey = "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"
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
        subject = "Redefinição de Senha - Smart Sun"

        # Use um nome padrão se o nome não for fornecido
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
