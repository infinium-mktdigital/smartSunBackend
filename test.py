import database, address

def getAddress(email,cep):

    try:
        request = database.getAddress(email)
        if request:
            return request
        response = address.searchCep(cep)
        database.saveAddress(email,response)
        lat_long = {
            "latitude": response['latitude'],
            "longitude": response['longitude']
        }
        return lat_long
    except Exception as e:
        return str(e)

email = "leonardo.oliveira@nappsolutions.com"
cep = "13613000"
response = getAddress(email, cep)
print(response)