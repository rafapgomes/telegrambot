import requests

def request(url,h,c,t):
    try:  
        response = requests.get(url,headers=h,cookies=c,timeout=t)
        return response.content
    except requests.ConnectTimeout:
        print("Erro")
        raise
   

