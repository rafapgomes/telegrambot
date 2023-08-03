import telebot
import cbf_scraper
import principal
import dicionariotimes
import os
from dotenv import load_dotenv
import requests.exceptions as re

load_dotenv()
chave_api = os.getenv("TOKEN")

bot = telebot.TeleBot(str(chave_api))


@bot.message_handler(commands=['start'])
def start(mensagem):
    bot.send_message(mensagem.chat.id,'Digite /time +sigla para ver os jogos recentes do Brasileirão Serie A ou B')
    bot.send_message(mensagem.chat.id,'Times disponivéis e suas siglas para acesso:')
    bot.send_message(mensagem.chat.id,'Série A')
    cont = 0
    for sig, time in dicionariotimes.siglas.items():
        bot.send_message(mensagem.chat.id,str(sig) +": "+str(time[0]))
        if(cont == 19):
                bot.send_message(mensagem.chat.id,'Série B')
        cont = cont +1

@bot.message_handler(commands=['time'])
def time(mensagem):

    time = " ".join(mensagem.text.split(" ")[1:])
    try:
        booleano = time.upper() in dicionariotimes.siglas
        print(booleano)
        if  not booleano:
            raise KeyError("Time não encontrado no dicionário.")

        bot.send_message(mensagem.chat.id,"Buscando informações de jogos do " + dicionariotimes.siglas[time.upper()][0] +", aguarde")
        try:
            info_time = cbf_scraper.get_rodada(time.upper())
        except re.ConnectTimeout:
            print('Nao foi possivel acessar o site da cbf')
            bot.send_message(mensagem.chat.id,"Nao foi possivel acessar o site da cbf, tente novamente")
            return -1
        except re.ReadTimeout:
             print('Nao foi possivel acessar os dados,tente novamente')
             bot.send_message(mensagem.chat.id,"Nao foi possivel acessar o site da cbf, tente novamente")
             return -1

        rodada = info_time['rodada']
        rodada = int(rodada)
        cont = rodada
        for i in range(cont-1,rodada + 3):
            try:
                info_jogo,transmissao = principal.envia_info_jogo(i,info_time)
            except re.ConnectTimeout:
                print('Nao foi possivel acessar o site da cbf')
                bot.send_message(mensagem.chat.id,"Nao foi possivel acessar o site da cbf, tente novamente")
                return -1
            except re.ReadTimeout:
             print('Nao foi possivel acessar os dados,tente novamente')
             bot.send_message(mensagem.chat.id,"Nao foi possivel acessar o site da cbf, tente novamente")
             return -1
            bot.send_message(mensagem.chat.id,'Rodada '+ str(i)  +'\n'+'Data:'+ info_jogo['desc']+'\n'+info_jogo['casa'] + " " + 
            info_jogo['info_geral'] + " " + info_jogo['fora']+'\n'+'Transmissao: '+transmissao)
    except KeyError as e:
        bot.send_message(mensagem.chat.id, "Erro: Time não encontrado")
        print("Erro:", e)


@bot.message_handler(func=lambda m: True)
def default(mensagem):
        bot.send_message(mensagem.chat.id,'Comando não reconhecido')
        bot.send_message(mensagem.chat.id,'Digite /time +sigla para ver os jogos recentes do Brasileirão Serie A ou B')
     

bot.polling()


    
