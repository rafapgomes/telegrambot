from os import kill
from typing import Text
from bs4 import BeautifulSoup as bs
from requests.api import get
import getpage
import unidecode
import dicionariotimes
headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}
cookies = {'cookie': 'cookie'}

#verifica em qual rodada o time está     
def get_rodada(user):
    page = getpage.request('https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a',headers,cookies)
    soup = bs(page,'html.parser')
    soup.find('tbody')
    for i in soup.find_all('tr',class_='expand-trigger'):
            time = i.find(class_='hidden-xs').contents[0]
            
            if  time == dicionariotimes.siglas[user]:
                    return {'rodada': i.find_all('td')[1].contents[0],'time':user}
               

#Retorna o jogo do time na rodada solicitada
def get_jogo(rodada,time):
    rodada = int(rodada)
    page =  page = getpage.request('https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a',headers,cookies)
    soup = bs(page,'html.parser')
    vetor = soup.find_all(class_='swiper-slide')
    if rodada >=38:
        return
    for i in vetor[rodada].find_all('li'):
        sigla = i.find_all('img')
        for k in sigla:
            if k['title'] == dicionariotimes.siglas[time]:
                   return i

#Retorna informações do jogo solicitado
def get_info_jogo(jogo):
    #Horario e local do jogo
    desc = jogo.find(class_='partida-desc text-1 color-lightgray p-b-15 block uppercase text-center')
    desc = str(desc.contents[0])
    desc = desc[30:47]
    #Pega o time da casa:
    time_casa = jogo.find(class_='time pull-left')     
    time_casa = time_casa.find(class_='time-sigla').contents[0]
    #Pega o time de fora:
    time_fora = jogo.find(class_='time pull-right')     
    time_fora = time_fora.find(class_='time-sigla').contents[0]
    res = jogo.find(class_='partida-horario center-block')
    #Testa se a tag onde fica o resultado/horario tem elemento filho
    childTag = res.find(class_='bg-blue color-white label-2')
    #Caso tenha, o jogo ja ocorreu. Pega o resultado.
    if childTag:
        info_geral = childTag.contents[0]
    #Caso contrario, o jogo não ocorreu. Pega o horario.
    else:
         info_geral = res.contents[0]
         info_geral = info_geral.strip()
    return {'desc':desc,'casa':time_casa,'fora':time_fora,'info_geral':info_geral}


get_jogo('2','CAM')