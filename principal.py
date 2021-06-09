import arq
import scrapepage
import twittervid
import cbf_scraper
#pega os links da midia do instagram
def get_insta_post(url):
    headers = { 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}
    cookies = {'sessionid':'2113549053%3ABmcfoaxek5Sg7A%3A29'}

    page = scrapepage.get_photo_page(url,headers,cookies)
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
    
def envia_info_jogos(update,info_time):
    rodada = info_time['rodada']
    time = info_time['time']
    num = int(rodada)+2
    for i in range(num):
        jogo = cbf_scraper.get_jogo(i,time)
        info = cbf_scraper.get_info_jogo(jogo)
        update.message.reply_text('Data:'+ info['desc'])
        update.message.reply_text(info['casa'] + " " + info['info_geral'] + " " + info['fora'])