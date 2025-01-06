import requests
from requests import cookies
def getCookies(url:str)-> cookies.RequestsCookieJar:
    """
    Auxiliary function used to get the cookies from the kaggle page.
    """
    r = requests.get(url)
    if r.status_code == 200:
        return r.cookies
    return None

def getUser(url:str):
    """
    Function used to get the data from the user page.
    """
    cookies = getCookies('https://www.kaggle.com/'+url)
    if not cookies:
        return 404
    dict_cookies = requests.utils.dict_from_cookiejar(cookies)
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-xsrf-token': dict_cookies['XSRF-TOKEN']
            }
    body = {
            'relativeUrl':'/'+url
            }
    response = requests.post(
            'https://www.kaggle.com/api/i/routing.RoutingService/GetPageDataByUrl',
            headers = headers,
            cookies = cookies,
            json = body
            )
    if response.status_code == 200:
        return response.status_code, response.json()
    return response.status_code

if __name__ == '__main__':
    url = 'msjimenezc'
    print(getUser(url))
    #getCookies(url)
