import logging
# from telegram.bot import Bot
from telegram.ext import CallbackContext,CommandHandler,Filters,MessageHandler
from flask import Flask, request
from telegram.ext.dispatcher import Dispatcher
from telegram import Update,Bot, ReplyKeyboardMarkup
from utils import get_reply, fetch_news, topics_keyboard

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = "2060372755:AAEDcL12uXIhiqJylKDB6dwV733PNj9mxA0"

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello!"

@app.route(f'/{TOKEN}', methods=['GET','POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    # process update
    dp.process_update(update)
    return "ok"

def start(update: Update, context: CallbackContext):
    print(update)
    author = update.message.from_user.first_name
    reply = "Howdy! {}".format(author)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply)

def _help(update: Update, context: CallbackContext):
    help_text = "Hey! This is a Help Text."
    context.bot.send_message(chat_id=update.message.chat_id,text =help_text)

def news(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Choose a Category", reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard,one_time_keyboard=True))

def reply_text(update: Update, context: CallbackContext):
    intent, reply = get_reply(update.message.text,update.message.chat_id)
    if intent == 'get_news':
        articles = fetch_news(reply)
        for article in articles:
            context.bot.send_message(chat_id=update.message.chat_id,text = article['link'])
    else:
        context.bot.send_message(chat_id=update.message.chat_id,text = reply)

def echo_sticker(update: Update, context: CallbackContext):
    context.bot.send_sticker(chat_id=update.message.chat_id,sticker=update.message.sticker.file_id)

def error(update: Update, context: CallbackContext):
    logger.error("Update '%s' caused error '%s'",update,context.error)

bot = Bot(TOKEN)
# updater = Updater(TOKEN,use_context=True)
try:
    bot.set_webhook("https://b3e5-122-160-51-56.ngrok.io/"+TOKEN)
except Exception as e:
    print(e)
dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",_help))
dp.add_handler(CommandHandler("news",news))
dp.add_handler(MessageHandler(Filters.text, reply_text))
dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
dp.add_error_handler(error)

if __name__=="__main__":
    
    app.run(port=8443)
