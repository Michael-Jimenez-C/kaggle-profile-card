import requests

def getUser(url:str):
    headers = {               
        'accept': 'application/json',
        'content-type': 'application/json',
        'cookie': 'CSRF-TOKEN=CfDJ8GXdT74sZy9Iv4qC0qaf2RcOnUOGoYrmfU8iK5Mnd2y7Q4H3tiuMB_62nZSnnykcGgBCdEC8z81bnfJ16mQx-BUfJXyZWQGPCi5O4aL9Og; GCLB=CPvy5tPX76rEzwEQAw.',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-xsrf-token': 'CfDJ8GXdT74sZy9Iv4qC0qaf2RewHckE3hVaWfJQWodyuVL518RzT_5Dwl_W-1sWp2AihOddV4l-QxpR1XGoyD2sE-kjiiYwkf0X6pr6uYt2uQehCg'
            }
    body = {
            'relativeUrl':'/'+url
            }

    response = requests.post(
            'https://www.kaggle.com/api/i/routing.RoutingService/GetPageDataByUrl',
            headers = headers,
            json = body
            )
    print(response.status_code)
    if response.status_code == 200:
        return response.status_code, response.json()
    return response.status_code
