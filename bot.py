import telebot
import cbf_scraper
import principal
import dicionariotimes
import os

chave_api = os.getenv("token")

bot = telebot.TeleBot(chave_api)


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
    
    bot.send_message(mensagem.chat.id,"Buscando informações de jogos do" + time +", aguarde")
    info_time = cbf_scraper.get_rodada(time.upper())
  
    rodada = info_time['rodada']
    rodada = int(rodada)
    cont = rodada
    for i in range(cont-1,rodada + 3):
       info_jogo,transmissao = principal.envia_info_jogo(i,info_time)
       bot.send_message(mensagem.chat.id,'Rodada '+ str(i)  +'\n'+'Data:'+ info_jogo['desc']+'\n'+info_jogo['casa'] + " " + 
                        info_jogo['info_geral'] + " " + info_jogo['fora']+'\n'+'Transmissao: '+transmissao)

bot.polling()

    
