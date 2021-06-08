import logging
import scrapepage
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import principal
import arq
import telegramkeys
import twittervid
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
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    update.message.reply_text('Ola! Eu sou um bot que baixa videos e fotos do Instagram! Digite /ig + link da midia e eu baixo pra você. Tambem baixo videos do twitter. Digite /tt e o link do video e eu baixo pra você')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


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


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    token = telegramkeys.token  
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(CommandHandler("ig",instagram))
    dispatcher.add_handler(CommandHandler("tt",twitter))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()