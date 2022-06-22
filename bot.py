import logging
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
    update.message.reply_text('Digite /time +sigla para ver os jogos recentes do Brasileirão Serie A ou B')
    update.message.reply_text('Times disponivéis e suas siglas para acesso:')
    for sig, time in dicionariotimes.siglas.items():
        update.message.reply_text(str(sig) +": "+str(time[0]))

          
          
          
    

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
    print(update.effective_user.id)
    update.message.reply


def time(update: Update, context: CallbackContext) -> None:
    info_time = cbf_scraper.get_rodada(context.args[0].upper())
    principal.envia_info_jogos(update,info_time)


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
    dispatcher.add_handler(CommandHandler("time",time))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
