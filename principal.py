import arq
import cbf_scraper

    
def envia_info_jogos(update,info_time):
    rodada = info_time['rodada']
    time = info_time['time']
    divisao = info_time['div']
    rodada = int(rodada)
    cont=rodada
    if cont > 0:
        cont=rodada-1
    num = int(rodada)+3
    for i in range(cont,num):
        jogo = cbf_scraper.get_jogo(i,time,divisao)
        info = cbf_scraper.get_info_jogo(jogo)
        link = info['link']
        transmissao = cbf_scraper.get_info_partida(link)
        update.message.reply_text('Rodada '+str(i+1)+'\n'+'Data:'+ info['desc']+'\n'+info['casa'] + " " + info['info_geral'] + " " + info['fora']+'\n'+'Transmissao: '+transmissao)
        

