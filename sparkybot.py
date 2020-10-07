# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import os
import time
from functools import wraps
import requests
from bs4 import BeautifulSoup
from telegram import ChatAction
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler, PicklePersistence)
from telegram.ext.dispatcher import run_async
from telegram.error import TelegramError, Unauthorized, RetryAfter

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
# stages
First, Second, Third = range(3)
# first stage callbackdata
Gl, Kr, Tw, Vn = range(4)
# second stage callback data
Bit32, Bit64 = range(2)

url1 = 'https://sparkcheats.tech'
url2 = 'https://sparkcheats.tech/download'
apk_name = 'SparkLoader'
ext = '.apk'
TOKEN = "1129141206:AAE64a9Msk0lKoDG3qSUcpckOzpMx8F7SN4"
# keyboard
reply_keyboard = [['Buy Key', 'Download Latest Loader'], ['Live ESP Status', 'Report Problem']]
file_id = ""

pp = PicklePersistence(filename='conversationbot',single_file= False)
# Decorator function for sending chat actions while processing func commands
def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator


# Function to handle /start command
@run_async
def start(update, context):
    user = update.message.from_user
    logger.info(" %s choosed  start option", user.first_name)
    data = context.user_data
    chat_id = update.message.chat.id
    data['user_id'] = chat_id
    update.message.reply_text(
        'Hi! My name is Sparky Bot.\n'
        'How may i help you ?\n\n\n'
        'Send /cancel to stop our conversation.\n'
        ,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return ConversationHandler.END


# when user clicks on Buy Key button
# @run_async
@send_action(ChatAction.TYPING)
@run_async
def Key(update, context):
    user = update.message.from_user
    logger.info(" %s choosed  key option", user.first_name)
    data = context.user_data
    chat_id = update.message.chat.id
    data['user_id'] = chat_id
    context.bot.forwardMessage(chat_id=update.message.chat_id, from_chat_id="-1001424216963", message_id="1787")
    update.message.reply_text('You can contact these resellers to buy your key')
@run_async
def Latest(update, context):
    user = update.message.from_user
    logger.info(" %s choosed  Latest option", user.first_name)
    context.bot.sendMessage(chat_id=update.message.chat_id,text="Okay Downloading Latest Loader")
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    file = requests.get(url2)
    url = requests.get(url1)
    soup = BeautifulSoup(url.text, 'lxml')
    version = soup.a.text[15:]
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    with open(apk_name + str(version) + ext, 'wb') as e:
        e.write(file.content)
    try:
        x = context.bot.send_document(chat_id=update.message.chat_id, document=open(apk_name + str(version) + ext, 'rb'))
        global file_id
        file_id = x.document.file_id
    except Exception as e:
        print(e)
        x.edit_text('Unable to Download Latest Loader 🥺.')
    filename = apk_name + str(version) + ext
    if os.path.exists(filename):
        os.remove(filename)
        print(filename, "deleted successfully")
    else:
        print("file not found")
# Deletes sparkcheats apk from storage

# def remove(filename):
#	if os.path.exists(filename):
#		os.remove(filename)
#		print(filename ,"delete successfully")
#	else:
#		print("file not found")


# Download+remove sparkcheats apk

@send_action(ChatAction.TYPING)
@run_async
def Download(update, context):
    user = update.message.from_user
    logger.info(" %s: downloaded latest apk", user.first_name)
    data = context.user_data
    chat_id = update.message.chat.id
    data['user_id'] = chat_id
    fname = user.first_name
    lname = user.last_name
    uname = user.username
    username = ""
    if uname == None:
    	username = None
    else:
    	username =f"@{uname}"
    reply_keyboard = [['Buy Key', 'Download Latest Loader'], ['Live ESP Status', 'Report Problem']]
    x = update.message.reply_text(text='Downloading please wait')#,reply_markup = ReplyKeyboardRemove(reply_keyboard))
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    # file = requests.get(url2)
    # url = requests.get(url1)
    # soup = BeautifulSoup(url.text, 'lxml')
    # version = soup.a.text[15:]
    # with open(apk_name + str(version) + ext, 'wb') as e:
    #     e.write(file.content)
    x.edit_text('Download successfull\nuploading now.')
    try:
        context.bot.send_document(chat_id=update.message.chat_id, document=file_id,
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                   resize_keyboard=True))
    except Exception as e:
        print(e)
        x.edit_text('Uploading failed.\n\nMy devs has been informed.\nPlease try after sometime')
        context.bot.sendMessage(chat_id="-491388645",text=f"uploading failed 🥺🥺 \nName  : {user.first_name} \nusername : {username}")

    # filename = apk_name + str(version) + ext
    # # remove(apk_name+str(version)+ext)
    # if os.path.exists(filename):
    #     os.remove(filename)
    #     print(filename, "delete successfully")
    # else:
    #     print("file not found")


# when user clicks on ESP Status button
# @run_async
@send_action(ChatAction.TYPING)
@run_async
def Status(update, context):
    user = update.message.from_user
    logger.info("%s selected  ESP STATUS", user.first_name)
    data = context.user_data
    chat_id = update.message.chat.id
    data['user_id'] = chat_id
    url = requests.get(url1)
    soup = BeautifulSoup(url.text, 'lxml')
    version1 = soup.p.text[:32]
    status1 = str(soup.p.text[33:])
    # nextsibling=soup.p.nextSibling
    # version2=nextsibling.text[:31]
    # status2=nextsibling.text[33:]
    all_p_tags = soup.find_all('p')
    time = all_p_tags[2].text
    time1 = time[:13]
    time2 = time[14:]
    update.message.reply_text(f"{version1}\n{status1}\n\n{time1}\n{time2}")


# cancel the conversation
# @run_async
@send_action(ChatAction.TYPING)
@run_async
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')
    # reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


# First level conversations starts here-------#
# @run_async
@send_action(ChatAction.TYPING)
@run_async
def Report(update, context):
    user = update.message.from_user
    logger.info("User %s started the conversation(Choosed Report Option).", user.first_name)
    data = context.user_data
    chat_id = update.message.chat.id
    data['user_id'] = chat_id
    keyboard = [
        [InlineKeyboardButton("Global", callback_data=str(Gl)),
         InlineKeyboardButton("kr", callback_data=str(Kr))],
        [InlineKeyboardButton("Tw", callback_data=str(Tw)),
         InlineKeyboardButton("Vn", callback_data=str(Vn))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Select your PUBG version",
        reply_markup=reply_markup
    )
    return First


# second level conversations---------#
# when user selects global option
# @run_async
@send_action(ChatAction.TYPING)
@run_async
def Pglobal(update, context):
    user = update.callback_query.from_user
    fname = user.first_name
    lname = user.last_name
    uname = user.username
    username = ""
    if uname == None:
    	username = None
    else:
    	username =f"@{uname}"
    name = f"{fname} {lname}"
    msg = f"Name : {name}\nusername : {username}\nchoosed PUBG Global "
    context.bot.sendMessage(chat_id="-491388645", text=msg)
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("32bit", callback_data=str(Bit32)),
         InlineKeyboardButton("64bit", callback_data=str(Bit64))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="You selected PUBG Global\n\n Now Select your  PUBG bit version",
        reply_markup=reply_markup
    )
    return Second


# when user selects kr option
# @run_async
@send_action(ChatAction.TYPING)
@run_async
def Pkr(update, context):
    user = update.callback_query.from_user
    fname = user.first_name
    lname = user.last_name
    uname = user.username
    username = ""
    if uname == None:
    	username = None
    else:
    	username =f"@{uname}"
    name = f"{fname} {lname}"
    msg = f"Name : {name}\nusername : {username}\nchoosed PUBG Kr"
    context.bot.sendMessage(chat_id="-491388645", text=msg)
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("32bit", callback_data=str(Bit32)),
         InlineKeyboardButton("64bit", callback_data=str(Bit64))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="You selected PUBG Kr\n\n Now Select your  PUBG bit version",
        reply_markup=reply_markup
    )
    return Second


# when user selects Tw option
# @run_async
@send_action(ChatAction.TYPING)
@run_async
def Ptw(update, context):
    user = update.callback_query.from_user
    fname = user.first_name
    lname = user.last_name
    uname = user.username
    username = ""
    if uname == None:
    	username = None
    else:
    	username =f"@{uname}"
    name = f"{fname} {lname}"
    msg = f"Name : {name}\nusername : {username}\nchoosed PUBG Tw "
    context.bot.sendMessage(chat_id="-491388645", text=msg)
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("32bit", callback_data=str(Bit32)),
         InlineKeyboardButton("64bit", callback_data=str(Bit64))
         ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="You selected PUBG tw\n\n Now Select your  PUBG bit version",
        reply_markup=reply_markup
    )
    return Second


# when user selects Vn option
# @run_async
@send_action(ChatAction.TYPING)
@run_async
def Pvn(update, context):
    user = update.callback_query.from_user
    fname = user.first_name
    lname = user.last_name
    uname = user.username
    username = ""
    if uname == None:
    	username = None
    else:
    	username =f"@{uname}"
    name = f"{fname} {lname}"
    msg = f"Name : {name}\nusername : {username}\nchoosed PUBG Vn"
    context.bot.sendMessage(chat_id="-491388645", text=msg)
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("32bit", callback_data=str(Bit32)),
         InlineKeyboardButton("64bit", callback_data=str(Bit64))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="You selected PUBG Vn\n\n Now Select your  PUBG bit version",
        reply_markup=reply_markup
    )
    return Second


# Third level conversations---------------#
# when user sects 32bit option
# @run_async
@send_action(ChatAction.TYPING)
@run_async
def Bit_32(update, context):
    user = update.callback_query.from_user
    fname = user.first_name
    lname = user.last_name
    uname = user.username
    username = ""
    if uname == None:
    	username = None
    else:
    	username =f"@{uname}"
    name = f"{fname} {lname}"
    msg = f"Name : {name}\nusername : {username}\nchoosed 32bit "
    context.bot.sendMessage(chat_id="-491388645", text=msg)
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Okay now describe your problem in a single message."
    )

    return Third


# when user selects 64 bit option
# @run_async
@send_action(ChatAction.TYPING)
@run_async
def Bit_64(update, context):
    user = update.callback_query.from_user
    fname = user.first_name
    lname = user.last_name
    uname = user.username
    username = ""
    if uname == None:
    	username = None
    else:
    	username =f"@{uname}"
    	
    name = f"{fname} {lname}"                                                                               
    msg = f"Name : {name}\nusername : {username}\nchoosed 64bit "
    context.bot.sendMessage(chat_id="-491388645", text=msg)
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Okay now describe your problem in a single message."
    )

    return Third


# Third level Conversation
# saves and send user inputs to our specified group/channel
# @run_async
@send_action(ChatAction.TYPING)
@run_async
def save_input(update, context):
    """Saves  and send input ."""
    for I in range(1):
        update.message.forward(chat_id="-491388645")
        update.message.reply_text("Thanks for reporting :)")
   # return True

@run_async
def send(update , context):
	user = update.message.from_user
	logger.info("User %s Choosed Send Option.", user.first_name)
	print("choosed send")
	message = update.message.reply_to_message.text
	context.bot.sendMessage(chat_id="-491388645",text='Okay sending!')
	active_user_count = 0
	blocked_user_count = 0
	for index , user_id in enumerate(pp.get_chat_data()):
		if index %28 == 0:
		    time.sleep(1)
		else:
			try:
				context.bot.sendMessage(chat_id= user_id, text= message)
				active_user_count += 1
			except Unauthorized as e:
				print(e)
				context.bot.sendMessage(chat_id= "-491388645",text=f"{e}.")
				blocked_user_count += 1
			except RetryAfter as r:
				print(f"Flood wait error at index: {index} and user id {user_id}.")
				print(r)
				time.sleep(r)
				context.bot.sendMessage(chat_id="-491388645", text = f"Completed Flood Wait of {r} Seconds.")
			except TelegramError as t:
				print(t)
				context.bot.sendMessage(chat_id="-491388645", text = f"Telegram error occured.\nThe error is :{t}.")
	context.bot.sendMessage(chat_id="-491388645",text=f"Successfully Sent to :\n{active_user_count} Active users 😎.\nBlocked users {blocked_user_count}😤.")
@run_async		
def broadcast(update, context):
	user = update.message.from_user
	logger.info("User %s Choosed broadcast option.", user.first_name)
	message_id = update.message.reply_to_message.message_id	
	update.message.reply_text("Okay! Broadcast Started")
	active_user_count = 0
	blocked_user_count = 0
	for index , user_id in enumerate(pp.get_chat_data()):
		if index %28 == 0:
		    time.sleep(1)
		else:
			try:
				#context.bot.sendMessage(chat_id= user_id, text= message)
				context.bot.forward_message(chat_id = user_id ,from_chat_id= update.message.chat_id, message_id = message_id)
				active_user_count += 1
			except Unauthorized as e:
				print(e)
				context.bot.sendMessage(chat_id= "-491388645",text=f"{e}.")
				blocked_user_count += 1
			except RetryAfter as r:
				print(f"Flood wait error at index: {index} and user id {user_id}.")
				print(r)
				time.sleep(r)
				context.bot.sendMessage(chat_id="-491388645", text = f"Completed Flood Wait of {r} Seconds.")
			except TelegramError as t:
				print(t)
				context.bot.sendMessage(chat_id="-491388645", text = f"Telegram error occured.\nThe error is :{t}.")
	context.bot.sendMessage(chat_id="-491388645",text=f"Successfully Broadcasted to :\n{active_user_count} Active  users 😎.\nBlocked users {blocked_user_count}😤.")

	#for i in pp.get_chat_data():
	#	context.bot.forward_message(chat_id = i ,from_chat_id= update.message.chat_id, message_id = message_id)

# main function
# @run_async
def main():
    updater = Updater(TOKEN,persistence=pp, use_context=True)    
    print("Bot started successfully")
    print("By @xcruzhd2")
    #print(pp.get_bot_data().keys())
   # for index , key in enumerate(pp.get_chat_data()):
	 #   print(index, key)
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Report Problem)$'), Report)],
        states={
            First: [CallbackQueryHandler(Pglobal, pattern='^' + str(Gl) + '$'),
                    CallbackQueryHandler(Pkr, pattern='^' + str(Kr) + '$'),
                    CallbackQueryHandler(Ptw, pattern='^' + str(Tw) + '$'),
                    CallbackQueryHandler(Pvn, pattern='^' + str(Vn) + '$')],
            Second: [CallbackQueryHandler(Bit_32, pattern='^' + str(Bit32) + '$'),
                     CallbackQueryHandler(Bit_64, pattern='^' + str(Bit64) + '$')],
            Third: [MessageHandler(Filters.all & ~Filters.command, save_input)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True,
        conversation_timeout=300
    )

    # Getting the dispatcher to register handlers
    dp = updater.dispatcher
 
       # registering handlers
    dp.add_handler(CommandHandler('broadcast', callback=broadcast,filters= Filters.chat(-491388645)))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex('^(Buy Key)$'), Key))
    dp.add_handler(MessageHandler(Filters.regex('^(Download Latest Loader)$'), Download))
    dp.add_handler(MessageHandler(Filters.regex('^(Live ESP Status)$'), Status))
    dp.add_handler(CommandHandler('cancel', cancel))
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('latest',callback=Latest,filters= Filters.chat(-491388645)))
    dp.add_handler(CommandHandler('send',callback=send,filters=Filters.chat(-491388645)))
        # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
