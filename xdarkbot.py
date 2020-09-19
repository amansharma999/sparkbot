
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
#import telegram
from telegram import ChatAction
import requests
import time
import requests
from bs4 import BeautifulSoup
import lxml
from functools import wraps
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler,CallbackQueryHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)




def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator




url1='https://sparkcheats.tech'
url2 ='https://sparkcheats.tech/download'
apk_name ='SparkLoader'
ext='.apk'
TOKEN="1129141206:AAE64a9Msk0lKoDG3qSUcpckOzpMx8F7SN4"

def start(update, context):
    reply_keyboard = [['Buy Key', 'Download Latest Loader'],['Live ESP Status','ReportProblem']]

    update.message.reply_text(
        'Hi! My name is Sparky Bot.\n'
        'How may i help you ?\n\n\n'
        'Send /cancel to stop talking to me.\n'
        ,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ConversationHandler.END

#@send_typing_action
@send_action(ChatAction.TYPING)
def Key(update, context):
    user = update.message.from_user
    logger.info(" %s choosed  %s option", user.first_name, update.message.text)
   # context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
    context.bot.forwardMessage(chat_id=update.message.chat_id,from_chat_id="-1001424216963",message_id="1787")
    
    update.message.reply_text('You can contact these resellers to buy your key')
    
def remove(filename):
	if os.path.exists(filename):
		os.remove(filename)
		print(filename ,"delete successfully")
	else:
		print("file not found")




@send_action(ChatAction.UPLOAD_DOCUMENT)
def Download(update, context):
    user = update.message.from_user
    #photo_file = update.message.photo[-1].get_file()
    #photo_file.download('user_photo.jpg')
    logger.info(" %s: downloaded latest apk", user.first_name )
    x = update.message.reply_text('Downloading.')
#    x= context.bot.send_message(text="Downloading.", chat_id=update.message.chat_id)
   # time.sleep(1)
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    context.bot.editMessageText(text='Downloading..', message_id = x.message_id, chat_id=update.message.chat_id)
   
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    file = requests.get(url2)
    url = requests.get(url1)
    soup = BeautifulSoup(url.text , 'lxml')
    version = soup.a.text[15:]
    context.bot.editMessageText(text='Downloading...', message_id = x.message_id, chat_id=update.message.chat_id)
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    with open(apk_name+str(version)+ext, 'wb') as e  :
    	e.write(file.content)
    #time.sleep(1)
    context.bot.editMessageText(text='Download successfull\nuploading now.', message_id = x.message_id, chat_id=update.message.chat_id)
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    context.bot.send_document(chat_id=update.message.chat_id, document=open(apk_name+str(version)+ext, 'rb'))
    remove(apk_name+str(version)+ext)
   # update.message.send_document(chat_id=update.message.chat_id, document=open(apk_name+str(version)+ext, 'rb'))
   # update.message.reply_text('Not Defined')

 
@send_action(ChatAction.TYPING)
def Status(update, context):
    user = update.message.from_user
#    user_location = update.message.location
    logger.info("%s selected  ESP STATUS", user.first_name)
    
    url=requests.get(url1)
    soup = BeautifulSoup(url.text , 'lxml')
    version1=soup.p.text[:32]
    status1=str(soup.p.text[33:])
    nextsibling=soup.p.nextSibling
    version2=nextsibling.text[:31]
    status2=nextsibling.text[33:]
    update.message.reply_text(f"{version1}\n{status1}\n\n{version2}\n{status2}")




def Report(update, context):
#    user = update.message.from_user
#    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Not Defined')

    return ConversationHandler.END

@send_action(ChatAction.TYPING)
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')
                              #reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN , use_context=True)
    print("Bot started successfully")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex('^(Buy Key)$'),Key))
    dp.add_handler(MessageHandler(Filters.regex('^(Download Latest Loader)$'),Download))
    dp.add_handler(MessageHandler(Filters.regex('^(Live ESP Status)$'), Status))
    dp.add_handler(MessageHandler(Filters.regex('^(Report Problem)$'),Report))
    dp.add_handler(CommandHandler('cancel', cancel))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
