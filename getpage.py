import requests

def request(url,h,c,t):
        response = requests.get(url,headers=h,cookies=c,timeout=t)
        return response.content
   

