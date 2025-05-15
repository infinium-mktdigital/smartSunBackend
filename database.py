import codes, time
from supabase import create_client, Client

supabase_url = "https://wcuiqirtagmefhrddcbe.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndjdWlxaXJ0YWdtZWZocmRkY2JlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY2NjMxMzAsImV4cCI6MjA2MjIzOTEzMH0.zhGCNmh0pl8DUUJ7ccCytAuFKKpr-sZpaWNtuU285GY"

supabase: Client = create_client(supabase_url, supabase_key)

def createUser(name, email, password):
    senha = codes.sha256(password)
    try:
        response = (
            supabase.table("users")
            .insert({"name": name, "email": email, "pass": senha})
            .execute()
        )
    except Exception as e:
        return str(e)
    return response


def searchUser(email, password):
    senha = codes.sha256(password)
    try:
        response = (
            supabase.table("users")
            .select("email")
            .eq("email",email)
            .eq("pass",senha)
            .execute()
        )
    except Exception as e:
        return str(e)
    return bool(response.data)

def resetPass(email):
    code = codes.forgetPass()  # Gera um código de 6 dígitos
    try:
        response = supabase.table("users").update({"pass_code": code}).eq("email", email).execute()
        if response.data:  # Verifica se o e-mail foi encontrado e atualizado
            return code
        else:
            return "E-mail não encontrado"
    except Exception as e:
        return str(e)

def deleteResetPass(email):
    try:
        supabase.table("users").upsert({"pass_code":""}).eq("email",email).execute()
    except Exception as e:
        return str(e)
    
def verifyPass(email,code):
    try:
        response = (
            supabase.table("users")
            .select("code")
            .eq("email",email)
            .eq("pass_code",code)
            .execute()
        )
    except Exception as e:
        return str(e)
    return bool(response.data)

def updatePass(email,password):
    senha = codes.sha256(password)
    try:
        response = (
            supabase.table("users")
            .update({"pass": senha})
            .eq("email",email)
            .execute()
        )
    except Exception as e:
        return str(e)
    return response

def getAllUsers():
    try:
        response = supabase.table("users").select("*").execute()
        return response
    except Exception as e:
        return str(e)
