import requests



def request(url,h,c):  

    response = requests.get(url,headers=h,cookies=c)
    return response.content

