import requests, solar, json

def searchCep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    data = response.json()
    street = data["logradouro"]
    city = data["localidade"]
    zone = data["uf"]
    concat = " ".join([street, city, zone])
    formated = concat.replace(" ", "+")
    request = searchLatLong(formated)
    request["data"]=data
    return request

def searchLatLong(queryString):
    headers = {"User-Agent":"FHOProject lpais@alunos.fho.edu.br"}
    url = f'https://nominatim.openstreetmap.org/search?q={queryString}&format=json'
    response = requests.get(url=url,headers=headers)
    data = response.json()
    results = {
        "latitude":data[0]['lat'],
        "longitude":data[0]['lon']
    }
    return results