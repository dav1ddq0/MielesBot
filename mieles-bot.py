
from telegram.ext import (Updater, CommandHandler, CallbackContext, 
ConversationHandler, MessageHandler, CallbackQueryHandler, Filters)
import qrcode
import os
from telegram import Chat, ChatAction, InlineKeyboardMarkup, InlineKeyboardButton, Update, KeyboardButton, bot
from telegram.files.inputmedia import InputMedia, InputMediaDocument
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
import json

INPUT_TEXT:int = 0;
UBUNTU: int = 1;
MANJARO_ID: int =2;
REPO: int = 3;
MENU: int = 5;


def main_menu(update: Update, context:CallbackContext):

    buttons = [[
        KeyboardButton("Linux Repos"),  KeyboardButton("Config Proxy Python")
    ],
    [        
        KeyboardButton("Config Proxy  npm ")
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


# def start(update: Update, context:CallbackContext):
#     update.message.reply_text(
#         text = 'Buenas, aquí podrás encontrar la mayoría de los sitios libres de costo\n',
#         reply_markup = InlineKeyboardMarkup([
#             [InlineKeyboardButton(text='🐧 Ubuntu Repo 🐧', callback_data='ubuntu')],
#             [InlineKeyboardButton(text='Python', callback_data='python')],
#             [InlineKeyboardButton(text='Facebook', url='https://facebook.com')]
#         ])
#     )



# def linux_callback_handler(update: Update, context: CallbackContext):
#     query = update.callback_query
#     query.answer()
#     query.edit_message_text(
#         text = 'Linux Repo',
#         reply_markup =  InlineKeyboardMarkup([
#             [InlineKeyboardButton(text='Ubuntu', callback_data='')],
#             [InlineKeyboardButton(text='how to use', callback_data = '2')]
#         ])
#     )

# def python_command_handler(update, context):
#     query = update.callback_query
#     query.answer()

#     query.edit_message_text(
#         text = 'Python Configuracion',
#         reply_markup =  InlineKeyboardMarkup([
#             [InlineKeyboardButton(text='proxy', callback_data='py')],
#             [InlineKeyboardButton(text='how to use', callback_data = '2')]
#         ])
#     )
    


# def qr_command_handler(update, context):
#     update.message.reply_text('Enviame el texto para generarte un codigo QR')
#     return INPUT_TEXT

# def qr_callback_handler(update, context):
#     query = update.callback_query
#     query.answer()
#     query.edit_message_text(
#         text ='Enviame el texto para generarte un codigo QR'
#     )
#     return INPUT_TEXT

# def ubuntu_callback_handler(update: Update, context: CallbackContext):
#     text = update.message.text
#     filename = generate_qr(text)
#     chat  = update.message.chat
#     print(chat)
#     # print(filename)
#     send_qr(filename, chat)
#     return ConversationHandler.END
   
   
    
    
    
    
    # return ConversationHandler.END

# def generate_qr(text: str):
#     filename = f'{text}.jpg'
#     img = qrcode.make(text)
#     img.save(filename)
#     return filename

# def send_qr(filename, chat: ChatAction):
    
#     chat.send_action(
#         action = ChatAction.UPLOAD_PHOTO,
#         timeout = None
#     )
#     chat.send_photo(
#         photo=open(filename, 'rb')
#     )

#     os.unlink(filename)

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
    

# def input_text(update: Update, context: CallbackContext):
#     text = update.message.text
#     filename = generate_qr(text)
#     chat  = update.message.chat
#     print(chat)
#     # print(filename)
#     send_qr(filename, chat)
#     return ConversationHandler.END 

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
                MessageHandler(filters = Filters.regex(r"^(Config Proxy Python)$"), callback = python_proxy)],
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
    