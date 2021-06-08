from bot import twitter
import arq
import scrapepage
import twittervid

#pega os links da midia do instagram
def get_insta_post(url):
    page = scrapepage.get_photo_page(url)
    json_text = scrapepage.get_json_media_page(page)
    vetor = scrapepage.get_download_link(json_text)
    return vetor

#envia multiplas midias
def envio_sidecar(update,vetor):
        cont=0
        for i in vetor:
            if i == 1:
                arq.download(vetor[cont+1],'midia/'+str(cont),'.jpeg')
                update.message.reply_photo(photo=open('midia/'+str(cont)+'.jpeg','rb'))
            elif i == 2:
                arq.download(vetor[cont+1],'midia/'+str(cont),'.mp4')
                update.message.reply_photo(video=open('midia/'+str(cont)+'.mp4','rb'))


            cont = cont+1
   
#envia unica foto
def envio_single_photo(update,vetor):
    arq.download(vetor,'midia/1','.jpeg')
    update.message.reply_photo(photo=open('midia/1.jpeg','rb'))

#envia unico video
def envio_single_video(update,vetor):
    arq.download(vetor,'midia/1','.mp4')
    update.message.reply_video(video=open('midia/1.mp4','rb'))

#envia unico video do twitter
def envio_twitter(update,url):

    id = twittervid.spliturl(url)
    print(id)
    url = twittervid.getvideourl(id)
    arq.download(url,'ttvid/1','.mp4')
    update.message.reply_text('Enviando video!')
    update.message.reply_video(video=open('ttvid/1.mp4','rb'))
    
