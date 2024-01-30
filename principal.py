import cbf_scraper
import requests.exceptions as re

def get_info_jogo(rodada,info_time):
    #desmembra as informações do time
    time = info_time['time']
    divisao = info_time['div']
    #pega as informações do jogo
    try:
        jogo = cbf_scraper.get_jogo(rodada,time,divisao)
    except re.ConnectTimeout:
        return -1
    except re.ReadTimeout:
        return -1
    if("rodada38" == jogo):
        return "rodada38","rodada38"
    info = cbf_scraper.get_info_jogo(jogo)
    
    link = info['link']
    transmissao = cbf_scraper.get_info_partida(link)
    #retorna as informações de um jogo
    return info,transmissao
     