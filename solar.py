import requests

def request(latitude,longitude):
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN",
        "community": "RE",
        "latitude": latitude,
        "longitude": longitude,
        "format": "JSON"
    }

    response = requests.get(url, params=params)
    data = response.json()
    min = minSolar(data)
    return min

def minSolar(solar):
    try:
        month = solar['properties']['parameter']['ALLSKY_SFC_SW_DWN']
        monthValues = {k: v for k, v in month.items() if k != 'ANN'}
        minMonth = min(monthValues, key=monthValues.get)
        minValue = monthValues[minMonth]
        return minValue
    except Exception as e:
        return {"error": str(e)}