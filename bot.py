import telebot
import principal
import dicionariotimes
from dotenv import load_dotenv
import requests.exceptions as re
import time_info
load_dotenv()
chave_api = "6964674281:AAEQtXNNnqSGi3FpwS_K1Ith_KP_inzxoAU"

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
    #verifica se o time digitado existe    
    if(time_info.verificar_time_existente == False):
         bot.send_message("Time nao encontrado,tente novamente")
         return

    bot.send_message(mensagem.chat.id,"Buscando informações de jogos do " + dicionariotimes.siglas[time.upper()][0] +", aguarde")
    #chama a funcao que pega as informacoes do time desejado
    info_time = time_info.get_info_time(time)
    if(info_time == -1):
        bot.send_message(mensagem.chat.id,"Ocorreu um erro,tente novamente")
        return
        
    rodada = info_time['rodada']
    rodada = int(rodada)
    cont = rodada
    for i in range(cont-1,rodada + 3):
        info_jogo,transmissao = principal.get_info_jogo(i,info_time)
        if(info_jogo  == -1 or transmissao == -1):
            bot.send_message(mensagem.chat.id,"Ocorreu um erro ao acessar as informações do jogo")
            return
        if(info_jogo == "rodada38"):
             bot.send_message(mensagem.chat.id,"Ultima rodada do campeonato foi mostrada acima")
             return
        bot.send_message(mensagem.chat.id,'Rodada '+ str(i)  +'\n'+'Data:'+ info_jogo['desc']+'\n'+info_jogo['casa'] + " " + 
        info_jogo['info_geral'] + " " + info_jogo['fora']+'\n'+'Transmissao: '+transmissao)


@bot.message_handler(func=lambda m: True)
def default(mensagem):
        bot.send_message(mensagem.chat.id,'Comando não reconhecido')
        bot.send_message(mensagem.chat.id,'Digite /time +sigla para ver os jogos recentes do Brasileirão Serie A ou B')
     

bot.polling()


    
