import codes, os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(dotenv_path='env/.env')

supabase_url = "https://wcuiqirtagmefhrddcbe.supabase.co"
supabase_key = os.getenv("SUPABASE_API_KEY")

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
    code = codes.forgetPass()
    try:
        response = supabase.table("users").update({"pass_code": code}).eq("email", email).execute()
        if response.data:
            return code
    except Exception as e:
        return str(e)
    
def verifyPass(email,code):
    try:
        response = (
            supabase.table("users")
            .select("pass_code")
            .eq("email",email)
            .execute()
        )
    except Exception as e:
        return str(e)
    if code == response.data[0]['pass_code']:
        return True
    return False

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

def getAddress(email):
    try:
        response = (
            supabase.table("address")
            .select("lat, lon")
            .eq("fk_email", email)
            .execute()
        )
    except Exception as e:
        return str(e)
    return response.data

def saveAddress(email, address):
    data = address["data"]
    lat = address["latitude"]
    lon = address["longitude"]
    try:
        response = (
            supabase.table("address")
            .insert({"fk_email": email,
                     "data": data, 
                     "lat": lat,
                     "lon": lon})
            .execute()
        )
    except Exception as e:
        return str(e)
    return response.data

def getSolar(lat,lon):
    try:
        response = (
            supabase.table("address")
            .select("solar")
            .eq("lat", lat)
            .eq("lon", lon)
            .execute()
        )
    except Exception as e:
        return str(e)
    return response.data

def saveSolar(email, solar):
    try:
        response = (
            supabase.table("address")
            .update({"solar": solar})
            .eq("fk_email", email)
            .order("solar", desc=True)
            .execute()
        )
    except Exception as e:
        return str(e)
    return response.data