import json
import getpage
from bs4 import BeautifulSoup as bs

#Faz o reuqest pela pagina da midia
def get_photo_page(url):
   return getpage.request(url)

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