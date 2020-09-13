#Made by @xcruzhd2
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from telegram import ReplyMarkup

updater = Updater(token="1129141206:AAE64a9Msk0lKoDG3qSUcpckOzpMx8F7SN4")


dispatcher = updater.dispatcher



def start(bot, update):
    keyboard = [['setting'] , ['example'] ,[ 'about us']]
    bot.sendMessage(chat_id=update.message.chat_id , text='choose on of these keyboards' , 
    reply_markup = ReplyKeyboardMarkup(keyboard , resize_keyboard = True , one_time_keyboard = True))
  #  bot.send_message(chat_id=update.message.chat_id, text="Hello, Welcome 😎")
 
 




start_handler = CommandHandler("start", start)

dispatcher.add_handler(start_handler)


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text.upper())



echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)

dispatcher.add_handler(echo_handler)


def option(bot, update):
    button = [
        [InlineKeyboardButton("Option 1", callback_data="1"),
         InlineKeyboardButton("Option 2", callback_data="2")],
        [InlineKeyboardButton("Option 3", callback_data="3")]
    ]
    reply_markup = InlineKeyboardMarkup(button)

    bot.send_message(chat_id=update.message.chat_id,
                     text="Choose one option..",
                     reply_markup=reply_markup)


option_handler = CommandHandler("option", option)
dispatcher.add_handler(option_handler)




updater.start_polling()
