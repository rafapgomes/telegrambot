import getpage
import json


#Pega o ID dos stories do usuario
def get_stories_info_page(url,headers,cookies):
    response = getpage.request(url,headers,cookies)
    obj_json = json.loads(response)
    return obj_json['user']['id']


#Pega pagina com os stories

def get_stories_page(url,headers,cookies,userid):
    response = getpage.request(url,headers,cookies)
    obj_json = json.loads(response)
    return obj_json['reels'][userid]["items"]
#Extrai o ID do stories e o nome de usuario
def split_link(url):
    info = url.split("/",4)[4]
    user =info.split("/",1)[0]
    reels_id = info.split("/",1)[1]
    return {"reels_id":reels_id[0:19],"user":user}

#Acha o stories pelo ID
def nav_stories(obj_json,story_id):
    print(story_id)
    for item in obj_json:
        if item['pk'] == int(story_id):
            return item
#Pega link de download
def get_download_link(item):
    if item['media_type'] == 1:
         return {'url': item['image_versions2']['candidates'][0]['url'],'type': 1}
    elif item["media_type"] == 2:
          return {'url':item['video_versions'][0]['url'],'type':2}
