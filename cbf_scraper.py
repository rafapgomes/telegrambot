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
    divisao = dicionariotimes.siglas[user][1]
    page = getpage.request('https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-'+divisao,headers,cookies)
    soup = bs(page,'html.parser')
    soup.find('tbody')
    for i in soup.find_all('tr',class_='expand-trigger'):
            time = i.find(class_='hidden-xs').contents[0]
            
            if  time == dicionariotimes.siglas[user][0]:
                    return {'rodada': i.find_all('td')[1].contents[0],'time':user,'div':divisao}
               


#Retorna o jogo do time na rodada solicitada
def get_jogo(rodada,time,divisao):
    rodada = int(rodada)
    page =  page = getpage.request('https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-'+divisao,headers,cookies)
    soup = bs(page,'html.parser')
    vetor = soup.find_all(class_='swiper-slide')
    if rodada >=38:
        return
    for i in vetor[rodada].find_all('li'):
        sigla = i.find_all('img')
        for k in sigla:
            if k['title'] == dicionariotimes.siglas[time][0]:
                   return i

#Retorna informações do jogo solicitado
def get_info_jogo(jogo):
    #Horario e local do jogo
    desc = jogo.find(class_='partida-desc text-1 color-lightgray p-b-15 block uppercase text-center')
    desc = str(desc.contents[0])
    desc = desc[30:53]
    link_jogo = jogo.find(class_='no-underline')['href']
    print(link_jogo)
    #Pega o time da casa:
    time_casa = jogo.find(class_='time pull-left')     
    time_casa = time_casa.find('img')['title']
    #Pega o time de fora:
    time_fora = jogo.find(class_='time pull-right')     
    time_fora = time_fora.find('img')['title']
    res = jogo.find(class_='partida-horario center-block')
    #Testa se a tag onde fica o resultado/horario tem elemento filho
    childTag = res.find(class_='bg-blue color-white label-2')
    #Caso tenha, o jogo ja ocorreu. Pega o resultado.
    if childTag:
        info_geral = childTag.contents[0]
    else:
        info_geral= 'x'
    return {'desc':desc,'casa':time_casa,'fora':time_fora,'info_geral':info_geral,'link':link_jogo}

def get_info_partida(link):
    page = getpage.request(link,headers,cookies)
    soup = bs(page,'html.parser')
    lista =  soup.find_all(class_='text-2 p-r-20')
    return lista[-1].text
    