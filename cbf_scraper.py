from bs4 import BeautifulSoup as bs
import getpage
import dicionariotimes

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

cookies = {'cookie': 'cookie'}

#verifica em qual rodada o time está     
def get_rodada(user):
    divisao = dicionariotimes.siglas[user][1]
    page = getpage.request('https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-'+divisao,headers,cookies,5)
    soup = bs(page,'html.parser')
    soup.find('tbody')
    for i in soup.find_all('tr',class_='expand-trigger'):
            time = i.find(class_='hidden-xs').contents[0]

            if  time == dicionariotimes.siglas[user][0]:
                    return {'rodada': i.find_all('td')[1].contents[0],'time':user,'div':divisao}
               


#Retorna o jogo do time na rodada solicitada
def get_jogo(rodada,time,divisao):
    rodada = int(rodada)
    #faz a requisicao da pagina da cbf onde estao os dados
    page =  page = getpage.request('https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-'+divisao,headers,cookies,5)
    
    #pega o conteudo da pagina com o bs4
    soup = bs(page,'html.parser')
    vetor = soup.find_all(class_='swiper-slide')
    if rodada >37:
        return "rodada38"
    #pega o jogo em questao da lista da cbf, buscando atraves do nome do time
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

#Retorna informações de transmissao
def get_info_partida(link):
    page = getpage.request(link,headers,cookies,5)
    soup = bs(page,'html.parser')
    tag =  soup.find(class_='col-sm-4 text-right')
    childTag = tag.find(class_="text-2 p-r-20")
    if childTag:
        transmissao = childTag.text
    else:
        transmissao = 'Nao disponivel'
    return transmissao


           
            

    