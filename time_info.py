import cbf_scraper
import requests.exceptions as re
import principal
import dicionariotimes

#acessa a pagina da cbf para retornar infomacoes do time desejado
def get_info_time(time): 
    try:
        info_time = cbf_scraper.get_rodada(time.upper())
        return info_time
    except re.ConnectionError:
        print("erro de conexao")
        return -1
    except re.ReadTimeout:
        print("erro de leitura")
        return -1


def get_info_jogo(i,info_time):
    try:
        info_jogo,transmissao = principal.get_info_jogo(i,info_time)
        return info_jogo,transmissao
    except re.ConnectTimeout:
            return -1,-1
    except re.ReadTimeout:
        return -1,-1
    
def verificar_time_existente(time):
    try:
        return time.upper() in dicionariotimes.siglas
    except KeyError as e:
        print("Erro:", e)
        return False


    
    


