import json
import getpage
from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime




#Faz o reuqest pela pagina da midia
def get_photo_page(url,headers,cookies):
   return getpage.request(url,headers,cookies)
#Pega um novo seasonID
def login(user,senha):
    print(user)
    print(senha)
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"

            }
    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    time = int(datetime.now().timestamp())
    response = requests.get(link,headers=header)
    csrf = response.cookies['csrftoken']

    payload = {
    'username': user,
    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{senha}',
    'queryParams': {},
    'optIntoOneTap': 'false'
    }

    login_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/accounts/login/",
    "x-csrftoken": csrf
    }

    login_response = requests.post(login_url, data=payload, headers=login_header)
    json_data = json.loads(login_response.text)
    print(json_data)
    if json_data["authenticated"]:
        cookies = login_response.cookies
        cookie_jar = cookies.get_dict()
        session_id = cookie_jar['sessionid']
        return session_id
    else:
        print("login failed ", login_response.text)




#Pega o JSON da midia
def get_json_media_page(page):
    soup = bs(page,'html.parser')
    lista = soup.find_all('script')
    text = lista[15].contents[0]
    text = text.split(',',1)[1]
    return text[0:len(text)-2]
#Retorna  tipo da midia
def get_media_type(json_text):
    obj_json = json.loads(json_text)
    return obj_json['graphql']['shortcode_media']['__typename']  
#Pega o link de download da midia
def get_download_link(json_text):
    obj_json = json.loads(json_text)
    if get_media_type(json_text)== 'GraphImage':
        obj_json = json.loads(json_text)
        return {'url':obj_json['graphql']['shortcode_media']['display_url'],'tipo':1,'owner': obj_json['graphql']['shortcode_media']['owner']['full_name']}
       
    elif get_media_type(json_text) == 'GraphSidecar':
          return get_sidecar_single_media(obj_json['graphql']['shortcode_media'])
    elif get_media_type(json_text) == 'GraphVideo':
         print('oi')
         print(obj_json['graphql']['shortcode_media']['video_url'])
         return {'url':obj_json['graphql']['shortcode_media']['video_url'],'tipo':3,'owner': obj_json['graphql']['shortcode_media']['owner']['full_name']}



#Pega o link de downloads de multiplas midias
def get_sidecar_single_media(lista):
    vetor = []
    print('oi')
    for i in lista['edge_sidecar_to_children']['edges']:
        if i['node']['__typename']== 'GraphImage':
                vetor.append(1)
                vetor.append(i['node']['display_url'])

        elif i['node']['__typename'] == 'GraphVideo':
             vetor.append(2)
             vetor.append(i['node']['video_url'])
    return {'url':vetor,'tipo':2,'owner': lista['owner']['full_name']}
