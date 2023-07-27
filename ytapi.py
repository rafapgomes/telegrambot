from googleapiclient.discovery import build
import json
import pprint


ytapikey = 'AIzaSyA8VR0paydU1V8p2J7I6pFhyAUO9zURHSM'
youtube = build('youtube','v3',developerKey = ytapikey)

d
def busca_video(busca,idcanal):

    request = youtube.search().list(
            part="id,snippet",
            q= busca,
            channelId = idcanal
        )
    return  request.execute()
