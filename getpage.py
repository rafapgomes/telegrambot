import requests

def request(url,h,c,t):
    try:  
        response = requests.get(url,headers=h,cookies=c,timeout=t)
        return response.content
    except requests.ConnectTimeout:
        print("Erro, nao foi possivel acessar a pagina")
        raise
    except requests.ReadTimeout:
        print("Nao foi possivel acessar os dados")
        raise
   

