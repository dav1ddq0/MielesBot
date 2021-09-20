
from telegram.ext import (Updater, CommandHandler, CallbackContext, 
ConversationHandler, MessageHandler, CallbackQueryHandler, Filters)
import qrcode
import os
from telegram import Chat, ChatAction, InlineKeyboardMarkup, InlineKeyboardButton, Update, KeyboardButton, bot
from telegram.files.inputmedia import InputMedia, InputMediaDocument
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
import json

REPO, MENU = range (2)

def main_menu(update: Update, context:CallbackContext):

    buttons = [[
        KeyboardButton("Linux Repos"),  KeyboardButton("Config Proxy Python")
    ],
    [        
        KeyboardButton("Config npm Proxy"), KeyboardButton("Consumo Nacionales")
    ]]

    keyboardMarkup = ReplyKeyboardMarkup(buttons)

    update.message.reply_text("Elige tu miel:", reply_markup=keyboardMarkup)
    
    return MENU; 


def linux_inline_menu(update: Update, context:CallbackContext):
    # return ConversationHandler.END
    buttons = [
        [KeyboardButton(text='🐧 Ubuntu Repo 🐧'), KeyboardButton(text='🐧 Manjaro Repo 🐧')],
        [KeyboardButton(text='🐧 Fedora Repo 🐧'), KeyboardButton(text = 'Back')],     
    ]
    keyboardMarkup = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(
        text = 'Elige la distro que estas usando:\n',
        reply_markup = keyboardMarkup
    )
    return REPO;

def python_proxy(update: Update, context: CallbackContext):
    update.message.reply_text(
        text = ' python -m pip install <package> --index-url http://nexus.prod.uci.cu/repository/pypi-proxy/simple/ --trusted-host nexus.prod.uci.cu\n')
    chat = update.message.chat
    chat.send_action(
        action = ChatAction.UPLOAD_PHOTO,
        timeout = None
    )
    filename = './proxy/python/python-proxy.png'
    chat.send_photo(
        photo = open(filename, 'rb'),caption='Example'
    )   

def npm_proxy(update: Update, context: CallbackContext):
    update.message.reply_text(
        text = 'Configuración:'
    )
    update.message.reply_text(
        text = 'npm config set registry http://nexus.prod.uci.cu/repository/npm-proxy/\n'
    )


    

def send_file(filename: str, chat: Chat):
    chat.send_action(
        action = ChatAction.UPLOAD_DOCUMENT,
        timeout = None
    )
    
    chat.send_document(
        document = open(filename, 'rb')
    )

    # os.unlink(filename)
def send_ubuntu_repo(update: Update, context: CallbackContext):
    filename = './linux-files/ubuntu/sources.list'
    chat = update.message.chat
    send_file(filename, chat)
    

def send_manjaro_repo(update: Update, context: CallbackContext):
    filename = './linux-files/manjaro/pacman.conf'
    chat = update.message.chat
    send_file(filename, chat)

def send_fedora_repo(update: Update, context: CallbackContext):
    filename = './linux-files/fedora/yum.repos.d.zip'
    chat = update.message.chat
    send_file(filename, chat)

def nacionales(update: Update, context: CallbackContext):
    codeURL = "http://download.jovenclub.cu/aplicaciones/vscode/"
    chromeURL = "http://download.jovenclub.cu/aplicaciones/google-chrome/"
    joveclubURL = "http://download.jovenclub.cu/"



    inlineKeyboardMarkup = InlineKeyboardMarkup([
        [   InlineKeyboardButton(text = 'VSCode', url = codeURL),
            InlineKeyboardButton(text = 'Google Chrome', url = chromeURL)
        ],
        [InlineKeyboardButton(text = 'JovenClub', url = joveclubURL)]
    ])
    update.message.reply_text(
        text = 'Consumo de Datos Nacionales',
        reply_markup= inlineKeyboardMarkup
    )


def fallback(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Disculpa no te entiendo")

def main():
    f = open('token.json',)
    myToken = json.load(f)['token']
    f.close()
    updater = Updater(token=myToken, use_context=True)
    dp = updater.dispatcher
   
    dp.add_handler(ConversationHandler(
        entry_points=[          
            CommandHandler('start', main_menu)
            
        ],
        states={
            
            MENU: [MessageHandler(filters = Filters.regex(r"^(Linux Repos)$"), callback = linux_inline_menu),
                MessageHandler(filters = Filters.regex(r"^(Config Proxy Python)$"), callback = python_proxy),
                MessageHandler(filters = Filters.regex(r"^(Config npm Proxy)$"), callback = npm_proxy),
                MessageHandler(filters = Filters.regex(r"^(Consumo Nacionales)$"), callback = nacionales)]
                ,
            REPO: [
                MessageHandler(filters = Filters.regex(r'^🐧 Ubuntu Repo 🐧$'), callback=send_ubuntu_repo),
                MessageHandler(filters = Filters.regex(r'^🐧 Fedora Repo 🐧$'), callback=send_fedora_repo),
                MessageHandler(filters = Filters.regex(r'^🐧 Manjaro Repo 🐧$'), callback=send_manjaro_repo),
                MessageHandler(filters = Filters.regex(r'^Back$'), callback=main_menu)
            ]
        },
        fallbacks=[
            MessageHandler(filters = Filters.all, callback = fallback)
        ]
    ))
    # add  handler

    updater.start_polling()
    updater.idle()
    
    

if __name__ == '__main__':
    main()
    