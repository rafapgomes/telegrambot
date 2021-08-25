import logging
import igscraper
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import principal
import arq
import telegramkeys
import cbf_scraper
import dicionariotimes
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!'
       )
    update.message.reply_text('Ola! Eu sou um bot que baixa videos e fotos do Instagram!') 
    update.message.reply_text('Digite /ig + link da midia e eu baixo pra você. \n Tambem baixo videos do twitter. Digite /tt e o link do video e eu baixo pra você \n Digite /time +sigla para ver os jogos recentes do Brasileirão Serie A ou B')
    update.message.reply_text('Atenção: Funçao de dados de times em desenvolvimento,pode apresentar erros!')
    update.message.reply_text('Times disponivéis e suas siglas para acesso:')
    for sig, time in dicionariotimes.siglas.items():
        update.message.reply_text(str(sig) +": "+str(time[0]))

          
          
          
    

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
    print(Update.effective_user)



def instagram(update: Update, context: CallbackContext) -> None:
    vetor = principal.get_insta_post(context.args[0])
    #Baixa sidecar (publicações com multiplas midias juntas)
    if  vetor['tipo']==2:
            update.message.reply_text('Baixando multiplas midias de '+vetor['owner'])
            principal.envio_sidecar(update,vetor['url'])
            print('Envio completo!')
            arq.deleta('midia')
            print('Pasta limpa')

    #Baixa foto unica
    elif vetor['tipo']==1:
            print('foto unica')
            update.message.reply_text('Baixando a foto de '+vetor['owner'])
            principal.envio_single_photo(update,vetor['url'])
            print('Envio completo!')
            arq.deleta('midia')
            print('Pasta limpa')
    elif vetor['tipo']==3:
            print('video unica')

            update.message.reply_text('Baixando o video de '+vetor['owner'])
            print(vetor['url'])
            principal.envio_single_video(update,vetor['url'])
            print('Envio completo!')
            arq.deleta('midia')
            print('Pasta limpa')



def twitter(update: Update, context: CallbackContext) -> None:
    principal.envio_twitter(update,context.args[0])
    print('Envio completo!')
    arq.deleta('ttvid')
    print('Pasta limpa')

def time(update: Update, context: CallbackContext) -> None:
    info_time = cbf_scraper.get_rodada(context.args[0].upper())
    principal.envia_info_jogos(update,info_time)

def stories(update: Update, context: CallbackContext) -> None:
    principal.envia_stories(update,context.args[0])
    


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    token = telegramkeys.token  
    updater = Updater("1801533855:AAGpl_hLCl5cJU_EL2V0aEsIimei9k-LvKs")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(CommandHandler("ig",instagram))
    dispatcher.add_handler(CommandHandler("tt",twitter))
    dispatcher.add_handler(CommandHandler("time",time))
    dispatcher.add_handler(CommandHandler("stories",stories))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
