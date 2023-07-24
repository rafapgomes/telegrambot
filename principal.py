import cbf_scraper
import ytapi


def envia_info_jogo(rodada,info_time):
    #desmembra as informações do time
    time = info_time['time']
    divisao = info_time['div']
    #pega as informações do jogo
    jogo = cbf_scraper.get_jogo(rodada,time,divisao)
    info = cbf_scraper.get_info_jogo(jogo)
    link = info['link']
    transmissao = cbf_scraper.get_info_partida(link)
    #retorna as informações de um jogo
    return info,transmissao
     